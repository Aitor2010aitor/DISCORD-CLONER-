import sys
import traceback
import asyncio
import threading
import subprocess
import importlib
import json
import aiohttp

def install_if_missing(package_name, pip_name=None):
    if pip_name is None:
        pip_name = package_name
    try:
        importlib.import_module(package_name)
    except ImportError:
        print(f"Instalando {pip_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

install_if_missing("discord", "discord.py-self")

import tkinter as tk
from tkinter import messagebox, scrolledtext

try:
    import discord
    from discord import Client
except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"No se pudo importar discord: {e}\n\nEjecuta: pip install discord.py-self")
    sys.exit(1)

class ChannelSelector:
    def __init__(self, parent, channels):
        self.selected = []
        self.channels = channels

        self.window = tk.Toplevel(parent)
        self.window.title("Seleccionar canales para copiar mensajes")
        self.window.geometry("500x500")
        self.window.configure(bg="#2c2f33")
        self.window.transient(parent)
        self.window.grab_set()

        tk.Label(self.window, text="Selecciona los canales de donde copiar mensajes:",
                 fg="#ffffff", bg="#2c2f33", font=("Segoe UI", 11, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.window, bg="#2c2f33")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Seleccionar Todos", command=self.select_all,
                  bg="#7289da", fg="#ffffff", font=("Segoe UI", 9)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Ninguno", command=self.select_none,
                  bg="#747f8d", fg="#ffffff", font=("Segoe UI", 9)).pack(side="left", padx=5)

        list_frame = tk.Frame(self.window, bg="#2c2f33")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(list_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable = tk.Frame(self.canvas, bg="#1a1a2e")

        self.scrollable.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.check_vars = []
        for ch in channels:
            var = tk.BooleanVar(value=False)
            self.check_vars.append(var)
            frame = tk.Frame(self.scrollable, bg="#1a1a2e")
            frame.pack(fill="x", padx=5, pady=1)
            cb = tk.Checkbutton(frame, text=ch.name, variable=var,
                               fg="#ffffff", bg="#1a1a2e", selectcolor="#40444b",
                               activebackground="#1a1a2e", activeforeground="#ffffff",
                               font=("Consolas", 10))
            cb.pack(anchor="w")

        confirm_btn = tk.Button(self.window, text="CONFIRMAR", command=self.confirm,
                                bg="#43b581", fg="#ffffff", font=("Segoe UI", 12, "bold"))
        confirm_btn.pack(pady=10, ipadx=20, ipady=5)

        self.window.wait_window()

    def select_all(self):
        for var in self.check_vars:
            var.set(True)

    def select_none(self):
        for var in self.check_vars:
            var.set(False)

    def confirm(self):
        self.selected = []
        for i, var in enumerate(self.check_vars):
            if var.get():
                self.selected.append(self.channels[i])
        self.window.destroy()


class CloneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Server Cloner")
        self.root.geometry("650x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c2f33")
        self.client = None
        self.selected_channels = []

        tk.Label(root, text="DISCORD SERVER CLONER", font=("Segoe UI", 16, "bold"),
                 fg="#7289da", bg="#2c2f33").pack(pady=10)

        tk.Label(root, text="Token de tu cuenta:", fg="#99aab5", bg="#2c2f33",
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        self.token_entry = tk.Entry(root, width=60, show="*", bg="#40444b",
                                     fg="#ffffff", insertbackground="#ffffff",
                                     font=("Consolas", 9))
        self.token_entry.pack(padx=20, pady=(0,8))

        frame = tk.Frame(root, bg="#2c2f33")
        frame.pack(padx=20, fill="x")

        tk.Label(frame, text="ID Origen:", fg="#ffffff", bg="#2c2f33",
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
        self.source_entry = tk.Entry(frame, width=30, bg="#40444b", fg="#ffffff",
                                      insertbackground="#ffffff", font=("Consolas", 10))
        self.source_entry.grid(row=0, column=1, padx=(10,0), pady=5)

        tk.Label(frame, text="ID Destino:", fg="#ffffff", bg="#2c2f33",
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
        self.dest_entry = tk.Entry(frame, width=30, bg="#40444b", fg="#ffffff",
                                    insertbackground="#ffffff", font=("Consolas", 10))
        self.dest_entry.grid(row=1, column=1, padx=(10,0), pady=5)

        self.community_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Activar Comunidad (anuncios, reglas, etc.)",
                       variable=self.community_var, fg="#ffffff", bg="#2c2f33",
                       font=("Segoe UI", 9), selectcolor="#40444b").pack(anchor="w", padx=20, pady=(8,0))

        self.messages_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Copiar mensajes con webhook (nombre y foto original)",
                       variable=self.messages_var, fg="#ffffff", bg="#2c2f33",
                       font=("Segoe UI", 9), selectcolor="#40444b").pack(anchor="w", padx=20)

        self.clone_btn = tk.Button(root, text="CLONAR SERVIDOR", font=("Segoe UI", 12, "bold"),
                                    bg="#43b581", fg="#ffffff", activebackground="#3ca374",
                                    cursor="hand2", command=self.start_clone)
        self.clone_btn.pack(pady=15, ipadx=20, ipady=5)

        tk.Label(root, text="Log:", fg="#99aab5", bg="#2c2f33",
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        self.log_text = scrolledtext.ScrolledText(root, height=8, width=75, bg="#1a1a2e",
                                              fg="#00ff41", font=("Consolas", 9),
                                              state="disabled", wrap="word")
        self.log_text.pack(padx=20, pady=(0,10))

        self.running = False

    def log(self, msg):
        def _update():
            self.log_text.config(state="normal")
            self.log_text.insert("end", msg + "\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
        self.root.after(0, _update)

    def set_btn(self, enabled):
        def _update():
            if enabled:
                self.clone_btn.config(state="normal", bg="#43b581")
            else:
                self.clone_btn.config(state="disabled", bg="#747f8d")
        self.root.after(0, _update)

    def start_clone(self):
        if self.running:
            return

        token = self.token_entry.get().strip()
        source_id = self.source_entry.get().strip()
        dest_id = self.dest_entry.get().strip()

        if not token:
            messagebox.showerror("Error", "Pega tu token")
            return
        if not source_id.isdigit():
            messagebox.showerror("Error", "ID origen invalido")
            return
        if not dest_id.isdigit():
            messagebox.showerror("Error", "ID destino invalido")
            return

        self.running = True
        self.set_btn(False)
        self.selected_channels = None
        self.log("Conectando...")

        t = threading.Thread(target=self.run_thread,
                             args=(token, int(source_id), int(dest_id),
                                   self.community_var.get(), self.messages_var.get()),
                             daemon=True)
        t.start()

    def run_thread(self, token, source_id, dest_id, copy_community, copy_messages):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.run_async(token, source_id, dest_id, copy_community, copy_messages))
        except Exception as e:
            self.log(f"ERROR: {e}")
            self.log(traceback.format_exc())
        finally:
            self.running = False
            self._http_session = None
            self.selected_channels = None

    def sanitize_embed(self, e):
        if not isinstance(e, dict):
            return None
        out = {}
        for k in ("title", "description", "url", "timestamp"):
            v = e.get(k)
            if v and str(v).strip():
                out[k] = str(v).strip()
        c = e.get("color")
        if isinstance(c, int):
            out["color"] = c
        footer = e.get("footer")
        if isinstance(footer, dict):
            ft = footer.get("text")
            fi = footer.get("icon_url")
            if ft or fi:
                out["footer"] = {}
                if ft:
                    out["footer"]["text"] = str(ft)
                if fi:
                    out["footer"]["icon_url"] = str(fi)
        author = e.get("author")
        if isinstance(author, dict):
            an = author.get("name")
            if an:
                out["author"] = {"name": str(an)}
        for k in ("image", "thumbnail"):
            obj = e.get(k)
            if isinstance(obj, dict):
                u = obj.get("url")
                if u:
                    out[k] = {"url": str(u)}
        fields_in = e.get("fields")
        if isinstance(fields_in, list):
            fields_out = []
            for f in fields_in:
                if not isinstance(f, dict):
                    continue
                n = f.get("name")
                v = f.get("value")
                if n and v:
                    fo = {"name": str(n), "value": str(v)}
                    if isinstance(f.get("inline"), bool):
                        fo["inline"] = f["inline"]
                    fields_out.append(fo)
            if fields_out:
                out["fields"] = fields_out
        return out or None

    async def run_async(self, token, source_id, dest_id, copy_community, copy_messages):
        self._http_session = aiohttp.ClientSession()
        self.client = Client()

        @self.client.event
        async def on_ready():
            try:
                self.log(f"Conectado: {self.client.user}")

                await asyncio.sleep(2)

                self.log(f"Servidores: {[g.name for g in self.client.guilds]}")

                source = self.client.get_guild(source_id)
                dest = self.client.get_guild(dest_id)

                if not source:
                    self.log(f"Error: servidor origen {source_id} no encontrado")
                    await self.client.close()
                    return
                if not dest:
                    self.log(f"Error: servidor destino {dest_id} no encontrado")
                    await self.client.close()
                    return

                if copy_messages:
                    select_channels = [ch for ch in source.text_channels]
                    if hasattr(source, 'forum_channels'):
                        select_channels += [ch for ch in source.forum_channels]
                    self.root.after(0, lambda: self.open_selector(select_channels))
                    while self.selected_channels is None:
                        await asyncio.sleep(0.1)

                try:
                    await self.clonar(source_id, dest_id, copy_community, copy_messages)
                except Exception as e:
                    self.log(f"ERROR clonar: {e}")
                    self.log(traceback.format_exc())
                finally:
                    try:
                        await self._http_session.close()
                    except:
                        pass
                    try:
                        await self.client.close()
                    except:
                        pass
            except Exception as e:
                self.log(f"ERROR on_ready: {e}")
                self.log(traceback.format_exc())
                try:
                    await self.client.close()
                except:
                    pass

        try:
            await self.client.start(token)
        except Exception as e:
            self.log(f"Error conexion: {e}")

    def open_selector(self, channels):
        selector = ChannelSelector(self.root, channels)
        self.selected_channels = selector.selected
        self.log(f"{len(self.selected_channels)} canales seleccionados para copiar mensajes")

    async def clonar(self, source_id, dest_id, copy_community, copy_messages):
        source = self.client.get_guild(source_id)
        dest = self.client.get_guild(dest_id)

        if not source:
            self.log("Error: Servidor origen no encontrado")
            return
        if not dest:
            self.log("Error: Servidor destino no encontrado")
            return

        self.log(f"Origen: {source.name} -> Destino: {dest.name}")

        # FOTO
        try:
            icon = await source.icon.read()
            await dest.edit(icon=icon)
            self.log("Foto copiada.")
        except Exception as e:
            self.log(f"Error foto: {e}")

        # NOMBRE
        try:
            if dest.name != source.name:
                await dest.edit(name=source.name)
                self.log(f"Nombre: {source.name}")
        except:
            pass

        # BORRAR CANALES
        self.log("Borrando canales...")
        for ch in list(dest.text_channels) + list(dest.voice_channels):
            try:
                await ch.delete()
                await asyncio.sleep(0.5)
            except:
                pass
        for ch in list(dest.categories):
            try:
                await ch.delete()
                await asyncio.sleep(0.5)
            except:
                pass

        # BORRAR ROLES
        self.log("Borrando roles...")
        for role in reversed(dest.roles):
            if role.name == "@everyone":
                continue
            try:
                await role.delete()
                await asyncio.sleep(0.5)
            except:
                pass

        # CLONAR ROLES
        self.log(f"Copiando {len(source.roles)} roles...")
        role_map = {}
        for role in reversed(source.roles):
            if role.name == "@everyone":
                role_map[role.id] = dest.default_role
                continue
            try:
                r = await dest.create_role(
                    name=role.name, color=role.color, hoist=role.hoist,
                    mentionable=role.mentionable, permissions=role.permissions
                )
                role_map[role.id] = r
                await asyncio.sleep(0.5)
            except Exception as e:
                self.log(f"Error rol {role.name}: {e}")

        self.log("Roles copiados.")

        # CATEGORIAS
        self.log("Copiando categorias y canales...")
        cat_map = {}
        for cat in source.categories:
            try:
                ow = {}
                for target, perm in cat.overwrites.items():
                    if target.id in role_map:
                        ow[role_map[target.id]] = perm
                    elif target.id == source.id:
                        ow[dest.default_role] = perm
                c = await dest.create_category(name=cat.name, overwrites=ow, position=cat.position)
                cat_map[cat.id] = c
                await asyncio.sleep(0.5)
            except Exception as e:
                self.log(f"Error cat {cat.name}: {e}")

        # CANALES
        channel_map = {}
        name_map = {}
        id_map = {}
        for ch in source.channels:
            try:
                ow = {}
                for target, perm in ch.overwrites.items():
                    if target.id in role_map:
                        ow[role_map[target.id]] = perm
                    elif target.id == source.id:
                        ow[dest.default_role] = perm

                cat = cat_map.get(ch.category_id)
                new_ch = None

                if isinstance(ch, discord.VoiceChannel):
                    new_ch = await dest.create_voice_channel(
                        name=ch.name, category=cat, overwrites=ow,
                        position=ch.position, bitrate=ch.bitrate, user_limit=ch.user_limit
                    )
                elif isinstance(ch, discord.TextChannel):
                    new_ch = await dest.create_text_channel(
                        name=ch.name, category=cat, overwrites=ow,
                        position=ch.position, topic=ch.topic
                    )

                if new_ch:
                    channel_map[ch.id] = new_ch
                    name_map[ch.name.lower()] = (ch, new_ch)
                    id_map[ch.id] = (ch, new_ch)

                await asyncio.sleep(0.5)
                self.log(f"  Canal: {ch.name}")
            except Exception as e:
                self.log(f"Error canal {ch.name}: {e}")

        # COMUNIDAD
        if copy_community:
            self.log("Configurando Comunidad...")
            try:
                if hasattr(source, 'rules_channel') and source.rules_channel:
                    src_rules = source.rules_channel
                    if src_rules.id in id_map:
                        _, dst_rules = id_map[src_rules.id]
                        try:
                            await dest.edit(rule_notifications_channel=dst_rules)
                        except:
                            pass

                if hasattr(source, 'public_updates_channel') and source.public_updates_channel:
                    src_updates = source.public_updates_channel
                    if src_updates.id in id_map:
                        _, dst_updates = id_map[src_updates.id]
                        try:
                            await dest.edit(public_updates_channel=dst_updates)
                        except:
                            pass

                if hasattr(source, 'description') and source.description:
                    try:
                        await dest.edit(description=source.description)
                    except:
                        pass

                self.log("Comunidad configurada.")
            except Exception as e:
                self.log(f"Error comunidad: {e}")

        # COPIAR MENSAJES SELECCIONADOS
        if copy_messages and self.selected_channels:
            self.log(f"Copiando mensajes de {len(self.selected_channels)} canal(es)...")

            # Dar permisos al usuario en los canales destino
            for src_ch in self.selected_channels:
                if src_ch.id in id_map:
                    _, dst_ch = id_map[src_ch.id]
                    try:
                        overwrites = dst_ch.overwrites.copy()
                        overwrites[dest.me] = discord.PermissionOverwrite(
                            read_messages=True, send_messages=True,
                            read_message_history=True, attach_files=True, embed_links=True
                        )
                        await dst_ch.edit(overwrites=overwrites)
                    except:
                        pass

            for src_ch in self.selected_channels:
                if not isinstance(src_ch, (discord.TextChannel, discord.ForumChannel)):
                    continue

                dst_ch = None
                if src_ch.id in id_map:
                    _, dst_ch = id_map[src_ch.id]

                if not dst_ch:
                    self.log(f"  {src_ch.name}: no encontrado en destino")
                    continue

                all_messages = []

                if isinstance(src_ch, discord.ForumChannel):
                    try:
                        for thread in src_ch.threads:
                            try:
                                async for msg in thread.history(limit=None, oldest_first=True):
                                    all_messages.append((thread, msg))
                            except:
                                try:
                                    before = None
                                    while True:
                                        url = f"/channels/{thread.id}/messages?limit=100"
                                        if before:
                                            url += f"&before={before}"
                                        data = await self.client.http.request(discord.http.Route("GET", url))
                                        if not data:
                                            break
                                        for m in data:
                                            msg = discord.Message(state=self.client._connection, channel=thread, data=m)
                                            all_messages.append((thread, msg))
                                        before = data[-1]["id"]
                                        if len(data) < 100:
                                            break
                                        await asyncio.sleep(0.3)
                                except:
                                    pass
                    except:
                        pass

                    try:
                        active_threads = await src_ch.active_threads()
                        for thread in active_threads:
                            if thread.id not in [t.id for t in src_ch.threads]:
                                try:
                                    async for msg in thread.history(limit=None, oldest_first=True):
                                        all_messages.append((thread, msg))
                                except:
                                    try:
                                        before = None
                                        while True:
                                            url = f"/channels/{thread.id}/messages?limit=100"
                                            if before:
                                                url += f"&before={before}"
                                            data = await self.client.http.request(discord.http.Route("GET", url))
                                            if not data:
                                                break
                                            for m in data:
                                                msg = discord.Message(state=self.client._connection, channel=thread, data=m)
                                                all_messages.append((thread, msg))
                                            before = data[-1]["id"]
                                            if len(data) < 100:
                                                break
                                            await asyncio.sleep(0.3)
                                    except:
                                        pass
                    except:
                        pass
                else:
                    try:
                        async for msg in src_ch.history(limit=None, oldest_first=True):
                            all_messages.append((None, msg))
                    except Exception:
                        try:
                            before = None
                            while True:
                                url = f"/channels/{src_ch.id}/messages?limit=100"
                                if before:
                                    url += f"&before={before}"
                                data = await self.client.http.request(discord.http.Route("GET", url))
                                if not data:
                                    break
                                for m in data:
                                    msg = discord.Message(state=self.client._connection, channel=src_ch, data=m)
                                    all_messages.append((None, msg))
                                before = data[-1]["id"]
                                if len(data) < 100:
                                    break
                                await asyncio.sleep(0.5)
                        except Exception as e:
                            self.log(f"  {src_ch.name}: no se pudo leer ({e})")
                            continue

                if not all_messages:
                    continue

                self.log(f"  {src_ch.name}: {len(all_messages)} mensajes")

                webhook = None
                try:
                    webhook = await dst_ch.create_webhook(name="Cloner")
                except:
                    pass

                if not webhook:
                    self.log(f"  {src_ch.name}: no se pudo crear webhook")
                    continue

                webhook_url = webhook.url
                if "?" not in webhook_url:
                    webhook_url += "?wait=true"

                thread_map = {}
                sent_messages = {}
                total_msgs = len(all_messages)

                for idx, (thread_or_none, msg) in enumerate(all_messages, 1):
                    try:
                        if idx % 10 == 0 or idx == total_msgs:
                            self.log(f"  {src_ch.name}: {idx}/{total_msgs} mensajes")

                        content = msg.content if msg.content else ""
                        username = msg.author.display_name
                        avatar_url = str(msg.author.display_avatar.url) if msg.author.display_avatar else None

                        image_exts = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp")

                        payload_embeds = []
                        files_to_send = []

                        for att in msg.attachments:
                            fname = att.filename.lower()
                            url = att.url

                            if fname.endswith(image_exts) or (att.content_type and att.content_type.startswith("image/")):
                                if len(payload_embeds) < 10:
                                    payload_embeds.append({"image": {"url": url}})
                            else:
                                try:
                                    async with self._http_session.get(url) as resp:
                                        if resp.status == 200:
                                            file_data = await resp.read()
                                            files_to_send.append((att.filename, file_data))
                                except:
                                    pass

                        for e in msg.embeds:
                            if len(payload_embeds) < 10:
                                clean = self.sanitize_embed(e.to_dict())
                                if clean:
                                    payload_embeds.append(clean)

                        if not content and not payload_embeds and not files_to_send:
                            continue

                        actual_webhook_url = webhook_url

                        if thread_or_none and isinstance(src_ch, discord.ForumChannel):
                            thread_name = thread_or_none.name
                            if thread_name not in thread_map:
                                try:
                                    if hasattr(dst_ch, 'create_thread'):
                                        forum_thread = await dst_ch.create_thread(
                                            name=thread_name,
                                            auto_archive_duration=10080
                                        )
                                        thread_map[thread_name] = forum_thread
                                    else:
                                        thread_map[thread_name] = None
                                except:
                                    thread_map[thread_name] = None

                            if thread_map.get(thread_name):
                                actual_webhook_url = webhook_url + f"&thread_id={thread_map[thread_name].id}"

                        payload_json = {"allowed_mentions": {"parse": []}}
                        if content:
                            payload_json["content"] = content[:2000]
                        if payload_embeds:
                            payload_json["embeds"] = payload_embeds[:10]
                        if username:
                            payload_json["username"] = username[:80]
                        if avatar_url:
                            payload_json["avatar_url"] = avatar_url

                        if msg.reference and msg.reference.message_id:
                            ref_id = str(msg.reference.message_id)
                            if ref_id in sent_messages:
                                ref_channel_id = str(thread_map[thread_or_none.name].id) if (thread_or_none and thread_or_none.name in thread_map and thread_map[thread_or_none.name]) else str(dst_ch.id)
                                payload_json["message_reference"] = {
                                    "message_id": sent_messages[ref_id],
                                    "channel_id": ref_channel_id
                                }

                        if not payload_json.get("content") and not payload_json.get("embeds") and not files_to_send:
                            continue

                        for _retry in range(3):
                            try:
                                payload_str = json.dumps(payload_json)
                                files_dict = {}
                                for i, (fname, fdata) in enumerate(files_to_send):
                                    files_dict[f"files[{i}]"] = (fname, fdata)

                                headers = {}
                                clean_url = actual_webhook_url.split("?")[0] + "?wait=true"

                                if files_dict:
                                    form = aiohttp.FormData()
                                    form.add_field("payload_json", payload_str, content_type="application/json")
                                    for key, (fn, fd) in files_dict.items():
                                        form.add_field(key, fd, filename=fn)
                                    async with self._http_session.post(clean_url, data=form, headers=headers) as resp:
                                        if resp.status == 429:
                                            data = await resp.json()
                                            wait = data.get("retry_after", 1)
                                            await asyncio.sleep(wait)
                                            continue
                                        if resp.status in (200, 201):
                                            try:
                                                resp_data = await resp.json()
                                                if resp_data and "id" in resp_data:
                                                    sent_messages[str(msg.id)] = resp_data["id"]
                                            except:
                                                pass
                                        elif resp.status >= 400:
                                            err = await resp.text()
                                            self.log(f"  Error {src_ch.name}: {resp.status} - {err[:100]}")
                                        break
                                else:
                                    async with self._http_session.post(clean_url, json=payload_json, headers=headers) as resp:
                                        if resp.status == 429:
                                            data = await resp.json()
                                            wait = data.get("retry_after", 1)
                                            await asyncio.sleep(wait)
                                            continue
                                        if resp.status in (200, 201):
                                            try:
                                                resp_data = await resp.json()
                                                if resp_data and "id" in resp_data:
                                                    sent_messages[str(msg.id)] = resp_data["id"]
                                            except:
                                                pass
                                        elif resp.status >= 400:
                                            err = await resp.text()
                                            self.log(f"  Error {src_ch.name}: {resp.status} - {err[:100]}")
                                        break
                            except Exception as e:
                                self.log(f"  Error envio: {e}")
                                break

                        await asyncio.sleep(0.5)
                    except:
                        pass

                try:
                    await webhook.delete()
                except:
                    pass

            self.log("Mensajes copiados.")

        self.log("CLONADO COMPLETADO!")

root = tk.Tk()
app = CloneApp(root)
root.mainloop()
