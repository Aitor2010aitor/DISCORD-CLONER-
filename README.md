[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Discord](https://img.shields.io/badge/Discord-Webhooks-5865F2?logo=discord&logoColor=white)](https://discord.com)
[![License](https://img.shields.io/badge/License-Educational%20Only-red)](#aviso-legal)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Copycord](https://img.shields.io/badge/Method-Copycord-purple)](https://github.com/Copycord/Copycord)

<div align="center">

# 🔥 DISCORD SERVER CLONER

### Clona servidores de Discord con un solo clic

[![Watch Demo](https://img.shields.io/badge/📋_Ver_Demo-grey?style=for-the-badge)](#cómo-funciona)
[![Download](https://img.shields.io/badge/⬇️_Descargar-grey?style=for-the-badge)](#instalación)
[![GitHub Stars](https://img.shields.io/github/stars/Aitor2010aitor/DISCORD-CLONER-?style=for-the-badge&logo=github)](https://github.com/Aitor2010aitor/DISCORD-CLONER-)
[![GitHub Forks](https://img.shields.io/github/forks/Aitor2010aitor/DISCORD-CLONER-?style=for-the-badge&logo=github)](https://github.com/Aitor2010aitor/DISCORD-CLONER-)

</div>

---

## ⚠️ AVISO LEGAL

> **Este proyecto es SOLO para fines educativos.** No me hago responsable del uso que le des a esta herramienta.
> 
> El uso de esta herramienta puede violar los [Términos de Servicio de Discord](https://discord.com/terms). Usar tu cuenta personal para automatizar acciones (selfbot) puede resultar en el **baneo permanente de tu cuenta**.

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Opciones](#opciones)
- [Cómo Funciona](#cómo-funciona)
- [Capturas](#capturas)
- [Tecnologías](#tecnologías)
- [Advertencia](#advertencia)

---

## 📝 Descripción

Herramienta educativa para clonar servidores de Discord. Copia **roles**, **canales**, **categorías**, **configuración de comunidad**, **mensajes** y **archivos** usando webhooks para mantener el nombre y avatar original de cada autor.

Basada en el método de envío por webhook de [Copycord](https://github.com/Copycord/Copycord).

---

## ✨ Características

<table>
<tr>
<td>

### 🏗️ Estructura
- ✅ Nombre del servidor
- ✅ Foto de perfil del servidor
- ✅ Roles con permisos y colores
- ✅ Categorías y canales de texto/voz
- ✅ Permisos por canal
- ✅ Configuración de Comunidad

</td>
<td>

### 💬 Mensajes
- ✅ Webhook con nombre y avatar del autor
- ✅ Imágenes como embeds (CDN directo)
- ✅ Archivos adjuntos reales (descarga y reenvío)
- ✅ Embeds sanitizados
- ✅ Threads de foros
- ✅ Manejo de rate limits

</td>
</tr>
</table>

---

## 📦 Requisitos

| Requisito | Versión |
|-----------|---------|
| Python | 3.10+ |
| discord.py-self | 2.1.0+ |
| aiohttp | 3.7.4+ |

---

## ⬇️ Instalación

### Opción 1: Automática (Recomendada)

Las dependencias se instalan automáticamente al ejecutar el script.

### Opción 2: Manual

```bash
pip install discord.py-self aiohttp
```

---

## 🚀 Uso

```bash
python clonar.py
```

### Pasos:

1️⃣ Ingresa el **token** de tu cuenta de Discord

2️⃣ Ingresa el **ID del servidor origen** (el que quieres copiar)

3️⃣ Ingresa el **ID del servidor destino** (donde se clonará)

4️⃣ Marca las opciones que quieras

5️⃣ Si marcaste "Copiar mensajes", se abrirá una ventana para **seleccionar canales**

6️⃣ Haz clic en **"CLONAR SERVIDOR"**

---

## ⚙️ Opciones

| Opción | Descripción |
|--------|-------------|
| ☑️ **Activar Comunidad** | Copia la configuración de Comunidad (canales de reglas, actualizaciones públicas, descripción) |
| ☑️ **Copiar mensajes con webhook** | Copia mensajes de canales de texto y foros usando webhooks |

---

## 🔍 Cómo Funciona

### Copia de Estructura

```
1. Borra todos los canales y roles del servidor destino
         ↓
2. Crea los roles del servidor origen en el destino
         ↓
3. Crea categorías y canales con los mismos permisos
```

### Copia de Mensajes (Webhook)

```
1. Crea un webhook temporal en cada canal seleccionado
         ↓
2. Envía cada mensaje con el nombre y avatar del autor original
         ↓
3. Las imágenes se envían como embeds (URL del CDN)
         ↓
4. Los archivos se descargan y reenvían como adjuntos reales
         ↓
5. Borra el webhook después de copiar
```

### Copia de Foros

```
1. Detecta todos los threads (activos y archivados)
         ↓
2. Crea threads en el destino con el mismo nombre
         ↓
3. Copia los mensajes de cada thread usando webhooks
```

---

## 📸 Capturas

<div align="center">

### Interfaz Principal
![Interfaz](https://via.placeholder.com/600x400/2c2f33/7289da?text=Discord+Server+Cloner+GUI)

### Selector de Canales
![Selector](https://via.placeholder.com/600x400/2c2f33/43b581?text=Channel+Selector)

</div>

---

## 🛠️ Tecnologías

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/Discord.py-self-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![aiohttp](https://img.shields.io/badge/aiohttp-2ECC71?style=for-the-badge&logo=asyncio&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-3498DB?style=for-the-badge&logo=python&logoColor=white)

</div>

---

## 📊 Estadísticas

<div align="center">

![GitHub watchers](https://img.shields.io/github/watchers/Aitor2010aitor/DISCORD-CLONER-?style=social)
![GitHub stars](https://img.shields.io/github/stars/Aitor2010aitor/DISCORD-CLONER-?style=social)
![GitHub forks](https://img.shields.io/github/forks/Aitor2010aitor/DISCORD-CLONER-?style=social)

</div>

---

## 🔗 Enlaces Útiles

- 📖 [Documentación de Discord.py](https://discordpy.readthedocs.io/)
- 🤖 [Discord Developer Portal](https://discord.com/developers/applications)
- 📦 [Copycord - Método original](https://github.com/Copycord/Copycord)

---

## 📄 Licencia

Este proyecto está bajo la licencia **Educational Use Only** - Ver [LICENSE](LICENSE) para más detalles.

---

## ⚠️ Advertencia Final

> **USO BAJO TU PROPIA RESPONSABILIDAD.**
> 
> Esta herramienta es solo para aprender sobre APIs y automatización. No la uses para fines maliciosos o que violen los términos de servicio de Discord.

---

<div align="center">

**Hecho con ❤️ para la comunidad educativa**

[![GitHub](https://img.shields.io/badge/GitHub-Aitor2010aitor-181717?style=for-the-badge&logo=github)](https://github.com/Aitor2010aitor)

</div>
