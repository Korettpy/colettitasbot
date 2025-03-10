import discord
import asyncio

TOKEN = "MTI3OTQ5NTQwMjcxMzkwNzM1NQ.GTEfLg.x8VXIBSMSgUQOAR_slTHBKG5P1YTNKfhamMy14"

# Mapeo de canales de origen y destino
CHANNEL_MAPPING = {
    1283988019166318605: 1152800232548085800,  # Canal A -> Canal X
    1283988021024395376: 1013005318659244072,
    1283988022345601179: 1316958187462594591# Canal B -> Canal Y
}

MAX_CHUNK_SIZE = 30  # Máximo de caracteres por fragmento
TARGET_CHANNEL_ID = 1013005318659244072  # Canal donde se enviarán los mensajes periódicos
MESSAGE_INTERVAL = 120  # Intervalo en segundos (ej. 1800 = 30 minutos)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

def split_message(text, max_length):
    """Divide el mensaje en fragmentos más pequeños sin cortar palabras."""
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        if len(current_chunk) + len(word) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = word
        else:
            current_chunk += (" " + word) if current_chunk else word

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')
    client.loop.create_task(periodic_messages())  # Iniciar tarea de mensajes periódicos

async def periodic_messages():
    """Envia mensajes periódicos a un canal específico."""
    await client.wait_until_ready()
    target_channel = client.get_channel(TARGET_CHANNEL_ID)
    
    while not client.is_closed():
        if target_channel:
            await target_channel.send("📢 Hola a todos bobis hablen revivire este server ya que mis circuitos detectaron inactividad.")
        await asyncio.sleep(MESSAGE_INTERVAL)  # Espera el intervalo antes de enviar de nuevo

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return  

    # Comando para enviar mensaje largo en fragmentos
    if message.content.startswith("!enviar "):  # Mensajes largos manuales
        texto = message.content[len("!enviar "):]
        message_chunks = split_message(texto, MAX_CHUNK_SIZE)

        for chunk in message_chunks:
            await message.channel.send(chunk, allowed_mentions=discord.AllowedMentions.all())
            await asyncio.sleep(1.5)  # Simula escritura

    # Verifica si el mensaje proviene de un canal de origen
    elif message.channel.id in CHANNEL_MAPPING:
        target_channel_id = CHANNEL_MAPPING[message.channel.id]
        target_channel = client.get_channel(target_channel_id)

        if target_channel:
            await target_channel.send(message.content, allowed_mentions=discord.AllowedMentions.all())
            for attachment in message.attachments:
                await target_channel.send(attachment.url)

client.run(TOKEN)
