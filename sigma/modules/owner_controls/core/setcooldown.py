# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord

from sigma.core.mechanics.command import SigmaCommand


async def setcooldown(cmd: SigmaCommand, message: discord.Message, args: list):
    command = None
    cooldown = None
    if args:
        if len(args) == 2:
            command = args[0].lower()
            if args[1].isdigit():
                cooldown = int(args[1])
        if command:
            if cooldown:
                if command in cmd.bot.modules.alts:
                    command = cmd.bot.modules.alts[command]
                if command in cmd.bot.modules.commands.keys():
                    cddata = {'command': command, 'cooldown': cooldown}
                    cd_coll = cmd.db[cmd.db.db_nam].CommandCooldowns
                    cddoc = await cd_coll.find_one({'Command': command})
                    if not cddoc:
                        await cd_coll.insert_one(cddata)
                    else:
                        await cd_coll.update_one({'command': command}, {'$set': cddata})
                    title = f'✅ Command {command} now has a {cooldown}s cooldown.'
                    response = discord.Embed(color=0x66CC66, title=title)
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 Command `{command}` not found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Missing or invalid cooldown.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing command to edit.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
