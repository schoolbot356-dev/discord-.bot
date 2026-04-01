import os
import discord
from discord.ext import commands
from discord import app_commands

# ===== CONFIGURACIÓN =====

# Usar variable de entorno para el token (seguro para GitHub y Railway)
TOKEN = os.environ.get("TOKEN")

OWNER_ID = 899839608030900225

ROLE_TAREAS_ID = 1489022058750017687
ROLE_EXAMENES_ID = 1489022252052779299
ROLE_RECORDATORIOS_ID = 1489022378955509933

# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ===== PANEL DE BOTONES =====

class PanelRoles(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def toggle_role(self, interaction, role_id):
        role = interaction.guild.get_role(role_id)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Se te quitó el rol **{role.name}**",
                ephemeral=True
            )
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"✅ Se te dio el rol **{role.name}**",
                ephemeral=True
            )

    @discord.ui.button(
        label="📚 Tareas",
        style=discord.ButtonStyle.primary,
        custom_id="panel_tareas"
    )
    async def tareas(self, interaction, button):
        await self.toggle_role(interaction, ROLE_TAREAS_ID)

    @discord.ui.button(
        label="📝 Exámenes",
        style=discord.ButtonStyle.success,
        custom_id="panel_examenes"
    )
    async def examenes(self, interaction, button):
        await self.toggle_role(interaction, ROLE_EXAMENES_ID)

    @discord.ui.button(
        label="⏰ Recordatorios",
        style=discord.ButtonStyle.secondary,
        custom_id="panel_recordatorios"
    )
    async def recordatorios(self, interaction, button):
        await self.toggle_role(interaction, ROLE_RECORDATORIOS_ID)


# ===== EVENTO READY =====

@bot.event
async def on_ready():
    bot.add_view(PanelRoles())
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

    print(f"Bot conectado como {bot.user}")


# ===== COMANDO !PANEL =====

@bot.command()
async def panel(ctx):
    if ctx.author.id != OWNER_ID:
        return

    embed = discord.Embed(
        title="📌 Panel de Notificaciones",
        description="Selecciona los roles para recibir avisos importantes:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📚 Tareas",
        value="Recibe avisos cuando se publiquen las tareas.",
        inline=False
    )
    embed.add_field(
        name="📝 Exámenes",
        value="Recibe avisos cuando se publiquen exámenes.",
        inline=False
    )
    embed.add_field(
        name="⏰ Recordatorios",
        value="Recibe avisos especiales importantes.",
        inline=False
    )

    embed.set_footer(text="Puedes activar o desactivar los roles cuando quieras.")

    await ctx.send(embed=embed, view=PanelRoles())


# ===== SLASH COMMAND /ARROZ =====

@bot.tree.command(name="arroz", description="Hace que el bot envíe un mensaje")
@app_commands.describe(mensaje="Mensaje que enviará el bot")
async def arroz(interaction: discord.Interaction, mensaje: str):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message(
            "No tienes permiso para usar este comando.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        "✅ Mensaje enviado.",
        ephemeral=True
    )

    await interaction.channel.send(mensaje)


# ===== INICIAR BOT =====

bot.run(TOKEN)
