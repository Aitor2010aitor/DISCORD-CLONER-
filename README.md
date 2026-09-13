# Discord Server Cloner

## ⚠️ AVISO LEGAL

**Este proyecto es SOLO para fines educativos.** No me hago responsable del uso que le des a esta herramienta.

El uso de esta herramienta puede violar los [Términos de Servicio de Discord](https://discord.com/terms). Usar tu cuenta personal para automatizar acciones (selfbot) puede resultar en el **baneo permanente de tu cuenta**.

## Descripción

Herramienta educativa para clonar servidores de Discord. Copia roles, canales, categorías, configuración de comunidad, mensajes y archivos usando webhooks para mantener el nombre y avatar original de cada autor.

Basada en el método de envío por webhook de [Copycord](https://github.com/Copycord/Copycord).

## Requisitos

- Python 3.10+
- Librería `discord.py-self`
- Librería `aiohttp`

## Instalación

Las dependencias se instalan automáticamente al ejecutar el script. Si falla:

```bash
pip install discord.py-self aiohttp
```

## Uso

```bash
python clonar.py
```

1. Ingresa el token de tu cuenta de Discord
2. Ingresa el ID del servidor origen (el que quieres copiar)
3. Ingresa el ID del servidor destino (donde se clonará)
4. Marca las opciones que quieras
5. Si marcaste "Copiar mensajes", se abrirá una ventana para seleccionar canales (texto y foros)
6. Haz clic en "CLONAR SERVIDOR"

## Opciones

- **Activar Comunidad**: Copia la configuración de Comunidad (canales de reglas, actualizaciones públicas, descripción)
- **Copiar mensajes con webhook**: Copia mensajes de canales de texto y foros. Usa webhooks para que cada mensaje tenga el nombre y avatar del autor original

## Funcionalidades

- Copia nombre del servidor
- Copia foto de perfil del servidor
- Copia todos los roles con permisos y colores
- Copia categorías y canales de texto/voz
- Copia permisos por canal
- Copia configuración de Comunidad
- Selector de canales para copiar mensajes (texto + foros)
- Copia mensajes usando webhooks (nombre y avatar del autor original)
- Copia imágenes como embeds (sin descargar)
- Copia archivos adjuntos reales (descarga y reenvía)
- Copia embeds sanitizados para webhooks
- Copia threads de foros con sus mensajes
- Manejo de rate limits (reintento automático en 429)
- Webhook temporal que se borra después del copiado

## Cómo funciona

### Copia de estructura
1. Borra todos los canales y roles del servidor destino
2. Crea los roles del servidor origen en el destino
3. Crea categorías y canales con los mismos permisos

### Copia de mensajes (Webhook)
1. Crea un webhook temporal en cada canal seleccionado
2. Envía cada mensaje con el nombre y avatar del autor original
3. Las imágenes se envían como embeds con la URL del CDN
4. Los archivos no-imagen se descargan y reenvían como adjuntos reales
5. Los embeds se sanitizan para compatibilidad con webhooks
6. Maneja rate limits automáticamente
7. Borra el webhook después de copiar

### Copia de foros
1. Detecta todos los threads (activos y archivados)
2. Crea threads en el destino con el mismo nombre
3. Copia los mensajes de cada thread usando webhooks

## Advertencia

**USO BAJO TU PROPIA RESPONSABILIDAD.** Esta herramienta es solo para aprender sobre APIs y automatización. No la uses para fines maliciosos o que violen los términos de servicio de Discord.
