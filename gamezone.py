import tkinter as tk
from tkinter import ttk, messagebox
import heapq
from collections import deque
from datetime import datetime
import random


BG = "black"
PANEL = "#151515"
PANEL2 = "#202020"
CARD = "#181818"
TEXT = "white"
MUTED = "#aaaaaa"
NEON = "#00ff99"
CYAN = "#00ccff"
PURPLE = "#b46cff"
RED = "#ff4d6d"
YELLOW = "#ffd54a"
GREEN = "#36e37b"

#Game 

class Game:
    def __init__(self, game_id, name, category, price, rating, description):
        self.game_id = game_id
        self.name = name
        self.category = category
        self.price = float(price)
        self.rating = float(rating)
        self.description = description
        self.featured = False

    def __str__(self):
        return self.name


#  Linked List 

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        if self.contains(data.game_id):
            return False
        node = Node(data)
        if self.head is None:
            self.head = node
        else:
            p = self.head
            while p.next:
                p = p.next
            p.next = node
        return True

    def remove(self, game_id):
        p = self.head
        prev = None
        while p:
            if p.data.game_id == game_id:
                if prev:
                    prev.next = p.next
                else:
                    self.head = p.next
                return True
            prev = p
            p = p.next
        return False

    def contains(self, game_id):
        p = self.head
        while p:
            if p.data.game_id == game_id:
                return True
            p = p.next
        return False

    def display(self):
        result = []
        p = self.head
        while p:
            result.append(p.data)
            p = p.next
        return result

    def calculate_total(self):
        total = 0
        p = self.head
        while p:
            total += p.data.price
            p = p.next
        return total

    def clear(self):
        self.head = None

    def count(self):
        n = 0
        p = self.head
        while p:
            n += 1
            p = p.next
        return n


#  Stack 
class Stack:
    def __init__(self):
        self.items = []

    def push(self, data):
        self.items.append(data)

    def pop(self):
        if self.items:
            return self.items.pop()
        return None

    def peek(self):
        if self.items:
            return self.items[-1]
        return None

    def display(self):
        return list(reversed(self.items))

    def count(self):
        return len(self.items)


#  Queue 
class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, data):
        self.items.append(data)

    def dequeue(self):
        if self.items:
            return self.items.popleft()
        return None

    def peek(self):
        if self.items:
            return self.items[0]
        return None

    def display(self):
        return list(self.items)

    def count(self):
        return len(self.items)


# Priority Queue

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def rebuild(self, games):
        self.heap = []
        for game in games:
            if game.featured:
                heapq.heappush(self.heap, (-game.rating, game.name.lower(), game.game_id, game))

    def push(self, game):
        if game.featured:
            heapq.heappush(self.heap, (-game.rating, game.name.lower(), game.game_id, game))

    def display(self):
        return [item[3] for item in sorted(self.heap)]

    def count(self):
        return len(self.heap)




# Admin 
class AdminPanel:
    def __init__(self, app):
        self.app = app
        self.logged_in = False
        self.window = None

    def open_login(self):
        win = tk.Toplevel(self.app.root)
        win.title("GAMEZONE - Admin Login")
        win.geometry("500x430")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.transient(self.app.root)
        win.grab_set()

        tk.Label(win, text="👨‍💼 ADMIN LOGIN", font=("Arial", 26, "bold"),
                 bg=BG, fg=NEON).pack(pady=(45, 10))
        tk.Label(win, text="Local demonstration login", bg=BG, fg=MUTED,
                 font=("Arial", 11)).pack(pady=(0, 25))

        form = tk.Frame(win, bg=PANEL)
        form.pack(fill="x", padx=45, pady=10)

        tk.Label(form, text="Username", bg=PANEL, fg=TEXT,
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=25, pady=(25, 5))
        user = tk.Entry(form, bg="#292929", fg=TEXT, insertbackground=TEXT,
                        font=("Arial", 12), relief="flat")
        user.pack(fill="x", padx=25, ipady=8)

        tk.Label(form, text="Password", bg=PANEL, fg=TEXT,
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=25, pady=(18, 5))
        password = tk.Entry(form, show="*", bg="#292929", fg=TEXT,
                            insertbackground=TEXT, font=("Arial", 12), relief="flat")
        password.pack(fill="x", padx=25, ipady=8)

        def login():
            if user.get().strip() == "admin" and password.get() == "admin123":
                win.destroy()
                self.logged_in = True
                self.open_dashboard()
            else:
                messagebox.showerror("Login Failed",
                                     "Invalid username or password.\n\nDemo:\nUsername: admin\nPassword: admin123")

        tk.Button(win, text="LOGIN", command=login, bg=NEON, fg="black",
                  activebackground="white", relief="flat", font=("Arial", 12, "bold"),
                  cursor="hand2", padx=35, pady=10).pack(pady=22)

    def open_dashboard(self):
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Toplevel(self.app.root)
        self.window.title("GAMEZONE - Admin Dashboard")
        self.window.geometry("1200x750")
        self.window.minsize(1050, 650)
        self.window.configure(bg=BG)
        self.window.protocol("WM_DELETE_WINDOW", self.logout)

        self.sidebar = tk.Frame(self.window, bg="#101010", width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="👨‍💼\nADMIN PANEL", bg="#101010",
                 fg=NEON, font=("Arial", 18, "bold")).pack(pady=25)

        buttons = [
            ("📊 Dashboard", self.dashboard),
            ("🎮 Games", self.manage_games),
            ("➕ Add Game", self.add_game),
            ("✏️ Edit Game", self.edit_game),
            ("🗑️ Delete Game", self.delete_game),
            ("⭐ Featured", self.featured),
            ("📦 Orders", self.orders),
            ("👥 Customers", self.customers),
            ("📈 Statistics", self.statistics),
            ("🧠 DSA Monitor", self.dsa_monitor),
            ("🚪 Logout", self.logout),
        ]
        for text, command in buttons:
            tk.Button(self.sidebar, text=text, command=command, bg="#101010",
                      fg=TEXT, activebackground="#292929", activeforeground=NEON,
                      relief="flat", anchor="w", font=("Arial", 10, "bold"),
                      padx=18, pady=9, cursor="hand2").pack(fill="x", padx=8, pady=2)

        self.content = tk.Frame(self.window, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)
        self.dashboard()

    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def title(self, text, subtitle=""):
        tk.Label(self.content, text=text, bg=BG, fg=TEXT,
                 font=("Arial", 25, "bold")).pack(anchor="w", padx=30, pady=(25, 3))
        if subtitle:
            tk.Label(self.content, text=subtitle, bg=BG, fg=MUTED,
                     font=("Arial", 10)).pack(anchor="w", padx=32, pady=(0, 18))

    def stat_card(self, parent, title, value, col):
        f = tk.Frame(parent, bg=PANEL, highlightthickness=1,
                     highlightbackground="#303030")
        f.grid(row=0, column=col, padx=8, sticky="nsew")
        tk.Label(f, text=title, bg=PANEL, fg=MUTED,
                 font=("Arial", 10, "bold")).pack(pady=(18, 5))
        label = tk.Label(f, text=value, bg=PANEL, fg=NEON,
                         font=("Arial", 22, "bold"))
        label.pack(pady=(0, 18))
        return label

    def dashboard(self):
        self.clear()
        self.title("👨‍💼 ADMIN DASHBOARD", "Welcome, Administrator! Live application statistics.")

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", padx=22)
        for i in range(4):
            cards.grid_columnconfigure(i, weight=1)

        revenue = sum(float(o["total"]) for o in self.app.orders_history)
        self.stat_card(cards, "🎮 Total Games", len(self.app.games), 0)
        self.stat_card(cards, "🛒 Cart Items", self.app.cart.count(), 1)
        self.stat_card(cards, "📦 Orders", len(self.app.orders_history), 2)
        self.stat_card(cards, "💰 Revenue", f"₹{revenue:,.0f}", 3)

        box = tk.Frame(self.content, bg=PANEL)
        box.pack(fill="both", expand=True, padx=30, pady=25)

        tk.Label(box, text="QUICK OVERVIEW", bg=PANEL, fg=CYAN,
                 font=("Arial", 15, "bold")).pack(anchor="w", padx=25, pady=20)

        data = [
            ("Games in Array", len(self.app.games)),
            ("Cart nodes in Linked List", self.app.cart.count()),
            ("Recently viewed Stack", self.app.recent.count()),
            ("Pending Queue", self.app.order_queue.count()),
            ("Featured Heap", self.app.featured_queue.count()),
            ("Game ID Hash Table", len(self.app.game_table)),
            ("Category Index", len(self.app.category_index)),
        ]
        for name, value in data:
            row = tk.Frame(box, bg=PANEL2)
            row.pack(fill="x", padx=25, pady=3)
            tk.Label(row, text=name, bg=PANEL2, fg=TEXT,
                     font=("Arial", 11)).pack(side="left", padx=15, pady=9)
            tk.Label(row, text=str(value), bg=PANEL2, fg=NEON,
                     font=("Arial", 11, "bold")).pack(side="right", padx=15)

        tk.Label(box, text="⚡ RECENT ACTIVITY", bg=PANEL, fg=YELLOW,
                 font=("Arial", 13, "bold")).pack(anchor="w", padx=25, pady=(18, 6))
        activity = self.app.activity_log if self.app.activity_log else ["No activity yet"]
        for item in activity[:5]:
            tk.Label(box, text="• " + item, bg=PANEL, fg=MUTED,
                     font=("Arial", 9), anchor="w").pack(fill="x", padx=30, pady=1)

    def make_tree(self, parent, columns, widths=None):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for i, c in enumerate(columns):
            tree.heading(c, text=c)
            tree.column(c, width=(widths[i] if widths else 120), anchor="center")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#171717", foreground="white",
                        fieldbackground="#171717", rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background="#292929",
                        foreground=NEON, font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#264d42")])
        return tree

    def manage_games(self):
        self.clear()
        self.title("🎮 MANAGE GAMES", "Edit, delete, or feature games.")
        frame = tk.Frame(self.content, bg=BG)
        frame.pack(fill="both", expand=True, padx=25, pady=5)
        tree = self.make_tree(frame, ("ID", "Game Name", "Category", "Price", "Rating", "Featured"),
                               [70, 230, 150, 110, 90, 100])
        tree.pack(fill="both", expand=True)

        for g in self.app.games:
            tree.insert("", "end", iid=str(g.game_id),
                        values=(g.game_id, g.name, g.category, f"₹{g.price:.0f}",
                                f"⭐ {g.rating:.1f}", "YES" if g.featured else "NO"))

        bar = tk.Frame(self.content, bg=BG)
        bar.pack(fill="x", padx=25, pady=15)

        def selected():
            ids = tree.selection()
            if not ids:
                messagebox.showwarning("Select Game", "Please select a game first.")
                return None
            return self.app.game_table.get(int(ids[0]))

        tk.Button(bar, text="✏️ Edit", command=lambda: self.edit_game(selected()),
                  bg=CYAN, fg="black", relief="flat", font=("Arial", 10, "bold"),
                  padx=20, pady=8).pack(side="left", padx=4)
        tk.Button(bar, text="🗑️ Delete", command=lambda: self.delete_game(selected()),
                  bg=RED, fg="white", relief="flat", font=("Arial", 10, "bold"),
                  padx=20, pady=8).pack(side="left", padx=4)
        tk.Button(bar, text="⭐ Feature / Unfeature",
                  command=lambda: self.toggle_feature(selected()),
                  bg=YELLOW, fg="black", relief="flat", font=("Arial", 10, "bold"),
                  padx=20, pady=8).pack(side="left", padx=4)
        tk.Button(bar, text="↻ Refresh", command=self.manage_games,
                  bg=PANEL2, fg=TEXT, relief="flat", font=("Arial", 10, "bold"),
                  padx=20, pady=8).pack(side="right", padx=4)

    def toggle_feature(self, game=None):
        if not game:
            return
        game.featured = not game.featured
        self.app.rebuild_structures()
        messagebox.showinfo("Featured", f"{game.name} is now "
                             f"{'featured' if game.featured else 'not featured'}.")
        self.manage_games()

    def add_game(self):
        self.clear()
        self.title("➕ ADD GAME", "Add a new game to the live collection.")

        self.game_form(mode="add")

    def edit_game(self, game=None):
        if isinstance(game, int):
            game = self.app.game_table.get(game)
        if game is None:
            self.clear()
            self.title("✏️ EDIT GAME", "Select a game to edit.")
            tree = self.make_tree(self.content, ("ID", "Game", "Category", "Price", "Rating"),
                                  [80, 260, 180, 120, 100])
            tree.pack(fill="both", expand=True, padx=30, pady=10)
            for g in self.app.games:
                tree.insert("", "end", iid=str(g.game_id),
                            values=(g.game_id, g.name, g.category, f"₹{g.price:.0f}",
                                    f"⭐ {g.rating:.1f}"))
            def open_selected():
                s = tree.selection()
                if not s:
                    messagebox.showwarning("Select Game", "Select a game first.")
                    return
                self.edit_game(self.app.game_table[int(s[0])])
            tk.Button(self.content, text="✏️ EDIT SELECTED", command=open_selected,
                      bg=CYAN, fg="black", relief="flat",
                      font=("Arial", 11, "bold"), padx=25, pady=10).pack(pady=10)
            return

        if not game:
            return
        self.clear()
        self.title("✏️ EDIT GAME", f"Editing Game ID {game.game_id}")
        self.game_form(mode="edit", game=game)

    def game_form(self, mode="add", game=None):
        form = tk.Frame(self.content, bg=PANEL)
        form.pack(fill="x", padx=35, pady=10)

        fields = [
            ("Game ID", str(game.game_id) if game else ""),
            ("Game Name", game.name if game else ""),
            ("Category", game.category if game else ""),
            ("Price", str(int(game.price)) if game else ""),
            ("Rating", str(game.rating) if game else ""),
            ("Description", game.description if game else ""),
        ]
        entries = {}
        for i, (label, value) in enumerate(fields):
            tk.Label(form, text=label, bg=PANEL, fg=TEXT,
                     font=("Arial", 10, "bold")).grid(row=i, column=0,
                                                       sticky="w", padx=25, pady=8)
            e = tk.Entry(form, bg="#292929", fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=("Arial", 11))
            e.insert(0, value)
            e.grid(row=i, column=1, sticky="ew", padx=25, pady=8, ipady=7)
            entries[label] = e
        form.grid_columnconfigure(1, weight=1)

        def save():
            gid = entries["Game ID"].get().strip()
            name = entries["Game Name"].get().strip()
            category = entries["Category"].get().strip()
            price = entries["Price"].get().strip()
            rating = entries["Rating"].get().strip()
            desc = entries["Description"].get().strip()

            if not gid.isdigit() or not name or not category or not price or not rating or not desc:
                messagebox.showerror("Invalid Data", "Please fill every field correctly.")
                return
            if not price.replace(".", "", 1).isdigit() or not rating.replace(".", "", 1).isdigit():
                messagebox.showerror("Invalid Data", "Price and rating must be numeric.")
                return

            gid = int(gid)
            price = float(price)
            rating = float(rating)

            if price < 0 or rating < 0 or rating > 5:
                messagebox.showerror("Invalid Data", "Price must be positive and rating must be 0–5.")
                return

            if mode == "add":
                if gid in self.app.game_table:
                    messagebox.showerror("Duplicate ID", "That Game ID already exists.")
                    return
                g = Game(gid, name, category, price, rating, desc)
                self.app.games.append(g)
                self.app.rebuild_structures()
                self.app.log_activity(f"Admin added {g.name}")
                messagebox.showinfo("Success", "✅ Game added successfully!")
                self.manage_games()
            else:
                if gid != game.game_id and gid in self.app.game_table:
                    messagebox.showerror("Duplicate ID", "That Game ID already exists.")
                    return
                old_id = game.game_id
                game.game_id = gid
                game.name = name
                game.category = category
                game.price = price
                game.rating = rating
                game.description = desc
                if old_id != gid:
                    self.app.rebuild_structures()
                else:
                    self.app.rebuild_structures()
                self.app.log_activity(f"Admin edited {game.name}")
                messagebox.showinfo("Success", "💾 Game updated successfully!")
                self.manage_games()

        tk.Button(self.content, text="💾 SAVE CHANGES" if mode == "edit" else "➕ ADD GAME",
                  command=save, bg=NEON, fg="black", relief="flat",
                  font=("Arial", 11, "bold"), padx=30, pady=10).pack(pady=20)

    def delete_game(self, game=None):
        if isinstance(game, int):
            game = self.app.game_table.get(game)
        if game is None:
            self.clear()
            self.title("🗑️ DELETE GAME", "Select a game to remove.")
            tree = self.make_tree(self.content, ("ID", "Game", "Category", "Price", "Rating"),
                                  [80, 260, 180, 120, 100])
            tree.pack(fill="both", expand=True, padx=30, pady=10)
            for g in self.app.games:
                tree.insert("", "end", iid=str(g.game_id),
                            values=(g.game_id, g.name, g.category, f"₹{g.price:.0f}",
                                    f"⭐ {g.rating:.1f}"))
            def remove_selected():
                s = tree.selection()
                if not s:
                    messagebox.showwarning("Select Game", "Select a game first.")
                    return
                self.delete_game(self.app.game_table[int(s[0])])
            tk.Button(self.content, text="🗑️ DELETE SELECTED", command=remove_selected,
                      bg=RED, fg="white", relief="flat",
                      font=("Arial", 11, "bold"), padx=25, pady=10).pack(pady=10)
            return

        if not game:
            return
        if not messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete {game.name}?"):
            return
        self.app.games = [g for g in self.app.games if g.game_id != game.game_id]
        self.app.log_activity(f"Admin deleted {game.name}")
        self.app.cart.remove(game.game_id)
        self.app.wishlist.discard(game.game_id)
        self.app.recent.items = [g for g in self.app.recent.items if g.game_id != game.game_id]
        self.app.rebuild_structures()
        messagebox.showinfo("Deleted", "🗑️ Game deleted successfully!")
        self.manage_games()

    def featured(self):
        self.clear()
        self.title("⭐ FEATURED GAMES", "Priority Queue / Heap — highest ratings first.")
        box = tk.Frame(self.content, bg=PANEL)
        box.pack(fill="both", expand=True, padx=30, pady=10)

        games = self.app.featured_queue.display()
        if not games:
            tk.Label(box, text="No featured games yet.", bg=PANEL, fg=MUTED,
                     font=("Arial", 14)).pack(pady=80)
            return
        for i, g in enumerate(games, 1):
            row = tk.Frame(box, bg=PANEL2)
            row.pack(fill="x", padx=20, pady=5)
            tk.Label(row, text=f"{i}.", bg=PANEL2, fg=YELLOW,
                     font=("Arial", 14, "bold"), width=4).pack(side="left", pady=12)
            tk.Label(row, text=g.name, bg=PANEL2, fg=TEXT,
                     font=("Arial", 12, "bold")).pack(side="left", padx=10)
            tk.Label(row, text=f"⭐ {g.rating:.1f}", bg=PANEL2, fg=YELLOW,
                     font=("Arial", 11, "bold")).pack(side="right", padx=20)

    def orders(self):
        self.clear()
        self.title("📦 ORDER MANAGEMENT", "Orders are processed using FIFO Queue.")
        tree = self.make_tree(self.content,
                              ("Order ID", "Customer", "Items", "Total", "Status"),
                              [100, 160, 330, 120, 130])
        tree.pack(fill="both", expand=True, padx=25, pady=10)

        for o in self.app.orders_history:
            tree.insert("", "end", iid=o["id"],
                        values=(o["id"], o["customer"], ", ".join(o["items"]),
                                f"₹{o['total']:.0f}", o["status"]))

        bar = tk.Frame(self.content, bg=BG)
        bar.pack(fill="x", padx=25, pady=12)

        def process():
            o = self.app.order_queue.dequeue()
            if not o:
                messagebox.showinfo("Queue Empty", "No pending orders.")
                return
            o["status"] = "Processing"
            messagebox.showinfo("Order Processing",
                                f"📦 {o['id']} is now Processing.")
            self.orders()

        def complete():
            s = tree.selection()
            if not s:
                messagebox.showwarning("Select Order", "Select an order.")
                return
            oid = s[0]
            for o in self.app.orders_history:
                if o["id"] == oid:
                    o["status"] = "Completed"
                    messagebox.showinfo("Completed", "✅ Order completed.")
                    self.orders()
                    return

        def cancel():
            s = tree.selection()
            if not s:
                messagebox.showwarning("Select Order", "Select an order.")
                return
            oid = s[0]
            for o in self.app.orders_history:
                if o["id"] == oid:
                    o["status"] = "Cancelled"
                    messagebox.showinfo("Cancelled", "❌ Order cancelled.")
                    self.orders()
                    return

        tk.Button(bar, text="📦 Process Next Order", command=process,
                  bg=CYAN, fg="black", relief="flat", font=("Arial", 10, "bold"),
                  padx=18, pady=8).pack(side="left", padx=4)
        tk.Button(bar, text="✅ Complete", command=complete,
                  bg=GREEN, fg="black", relief="flat", font=("Arial", 10, "bold"),
                  padx=18, pady=8).pack(side="left", padx=4)
        tk.Button(bar, text="❌ Cancel", command=cancel,
                  bg=RED, fg="white", relief="flat", font=("Arial", 10, "bold"),
                  padx=18, pady=8).pack(side="left", padx=4)

    def customers(self):
        self.clear()
        self.title("👥 CUSTOMERS", "Demo customer information from placed orders only.")
        tree = self.make_tree(self.content,
                              ("Customer", "Phone", "Orders", "Total Spent"),
                              [220, 180, 120, 180])
        tree.pack(fill="both", expand=True, padx=30, pady=10)

        data = {}
        for o in self.app.orders_history:
            name = o["customer"]
            if name not in data:
                data[name] = {"phone": o["phone"], "orders": 0, "spent": 0}
            data[name]["orders"] += 1
            data[name]["spent"] += o["total"]

        for name, d in data.items():
            tree.insert("", "end",
                        values=(name, d["phone"], d["orders"], f"₹{d['spent']:.0f}"))

    def statistics(self):
        self.clear()
        self.title("📈 SALES STATISTICS", "Calculated from current demo order data.")

        sold = sum(len(o["items"]) for o in self.app.orders_history)
        orders = len(self.app.orders_history)
        revenue = sum(o["total"] for o in self.app.orders_history)
        avg = revenue / orders if orders else 0

        counts = {}
        for o in self.app.orders_history:
            for item in o["items"]:
                counts[item] = counts.get(item, 0) + 1
        popular = max(counts, key=counts.get) if counts else "None"

        values = [
            ("🎮 Total Games Sold", sold),
            ("📦 Total Orders", orders),
            ("💰 Total Revenue", f"₹{revenue:,.2f}"),
            ("📊 Average Order Value", f"₹{avg:,.2f}"),
            ("🏆 Most Popular Game", popular),
        ]

        for label, value in values:
            row = tk.Frame(self.content, bg=PANEL)
            row.pack(fill="x", padx=50, pady=7)
            tk.Label(row, text=label, bg=PANEL, fg=TEXT,
                     font=("Arial", 13, "bold")).pack(side="left", padx=20, pady=15)
            tk.Label(row, text=str(value), bg=PANEL, fg=NEON,
                     font=("Arial", 14, "bold")).pack(side="right", padx=20)

    def dsa_monitor(self):
        self.clear()
        self.title("🧠 DSA SYSTEM STATUS", "Live structures used by GAMEZONE.")
        data = [
            ("Array / List", f"Games stored: {len(self.app.games)}"),
            ("Linked List", f"Cart nodes: {self.app.cart.count()}"),
            ("Stack", f"Recently viewed: {self.app.recent.count()}"),
            ("Queue", f"Pending orders: {self.app.order_queue.count()}"),
            ("Priority Queue / Heap", f"Featured games: {self.app.featured_queue.count()}"),
            ("Hash Table", f"Game IDs: {len(self.app.game_table)}"),
            ("Category Index", f"Categories: {len(self.app.category_index)}"),
        ]
        for name, value in data:
            row = tk.Frame(self.content, bg=PANEL)
            row.pack(fill="x", padx=35, pady=5)
            tk.Label(row, text=name, bg=PANEL, fg=CYAN,
                     font=("Arial", 12, "bold"), width=28, anchor="w").pack(side="left", padx=15, pady=12)
            tk.Label(row, text=value, bg=PANEL, fg=TEXT,
                     font=("Arial", 11)).pack(side="left")

        tk.Label(self.content, text="Search = Linear Search    |    Sorting = Bubble / Selection / Insertion",
                 bg=BG, fg=MUTED, font=("Arial", 10)).pack(pady=20)

    def logout(self):
        self.logged_in = False
        if self.window and self.window.winfo_exists():
            self.window.destroy()
        self.window = None


# Main App 

class GameShop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GAMEZONE — Ultimate Game Shop")
        self.root.geometry("1200x750")
        self.root.minsize(950, 620)
        self.root.configure(bg=BG)

        self.games = [
            Game(101, "GTA V", "Action", 1499, 4.9, "Open-world action adventure game."),
            Game(102, "Minecraft", "Adventure", 999, 4.8, "Build, explore and survive in a block-based world."),
            Game(103, "Valorant", "Shooter", 0, 4.7, "Competitive tactical hero shooter."),
            Game(104, "FIFA", "Sports", 1299, 4.6, "Fast-paced football experience."),
            Game(105, "Forza Horizon", "Racing", 1799, 4.7, "Open-world festival racing experience."),
            Game(106, "Need for Speed", "Racing", 899, 4.5, "High-speed street racing adventure."),
            Game(107, "Red Dead Redemption", "Adventure", 1999, 4.9, "Epic western open-world adventure."),
            Game(108, "Fortnite", "Battle Royale", 0, 4.5, "Build, battle and survive in a colorful arena."),
            Game(109, "PUBG", "Battle Royale", 799, 4.4, "Competitive battle royale action."),
            Game(110, "Call of Duty", "Shooter", 1199, 4.6, "Classic military shooter experience."),
            Game(111, "The Witcher", "Adventure", 1499, 4.7, "Fantasy role-playing adventure."),
            Game(112, "Cyberpunk 2077", "RPG", 1599, 4.6, "Futuristic open-world role-playing game."),
            Game(113, "Assassin's Creed", "Action", 1099, 4.5, "Stealth action in historic worlds."),
            Game(114, "Rocket League", "Sports", 699, 4.4, "Football with rocket-powered cars."),
            Game(115, "Among Us", "Casual", 299, 4.3, "Social deduction multiplayer game."),
            Game(116, "Terraria", "Adventure", 499, 4.6, "Explore, craft and fight in a 2D sandbox."),
            Game(117, "Roblox", "Casual", 0, 4.2, "A platform of user-created games and experiences."),
            Game(118, "Elden Ring", "RPG", 2499, 4.9, "Challenging fantasy action RPG."),
            Game(119, "Mortal Kombat", "Fighting", 999, 4.5, "Intense fighting game experience."),
            Game(120, "Far Cry", "Action", 899, 4.4, "Open-world action and exploration."),
        ]

        # Actual DSA structures
        self.cart = LinkedList()
        self.recent = Stack()
        self.order_queue = Queue()
        self.featured_queue = PriorityQueue()
        self.game_table = {}
        self.category_index = {}
        self.wishlist = set()
        self.orders_history = []
        self.activity_log = []
        self.order_number = 1001

        self.admin = AdminPanel(self)
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All")
        self.sort_var = tk.StringVar(value="Default")
        self.status_var = tk.StringVar(value="Welcome to GAMEZONE")
        self.current_games = list(self.games)

        self.setup_styles()
        self.rebuild_structures()
        self.build_shell()
        self.show_home()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass
        style.configure("TCombobox", fieldbackground="#292929",
                        background="#292929", foreground="white")
        style.map("TCombobox", fieldbackground=[("readonly", "#292929")],
                  foreground=[("readonly", "white")])

    def rebuild_structures(self):
        self.game_table = {g.game_id: g for g in self.games}
        self.category_index = {}
        for g in self.games:
            if g.category not in self.category_index:
                self.category_index[g.category] = []
            self.category_index[g.category].append(g.game_id)

        # Priority Queue is rebuilt from actual featured flags
        self.featured_queue.rebuild(self.games)

    #  Shell 
    def build_shell(self):
        self.topbar = tk.Frame(self.root, bg="#101010", height=72)
        self.topbar.pack(side="top", fill="x")
        self.topbar.pack_propagate(False)

        tk.Label(self.topbar, text="🎮 GAMEZONE", bg="#101010", fg=NEON,
                 font=("Arial", 23, "bold")).pack(side="left", padx=25)

        tk.Button(self.topbar, text="🏠 Home", command=self.show_home,
                  **self.nav_button()).pack(side="left", padx=3)
        tk.Button(self.topbar, text="🎮 Games", command=self.show_games,
                  **self.nav_button()).pack(side="left", padx=3)
        tk.Button(self.topbar, text="🛒 Cart", command=self.show_cart,
                  **self.nav_button()).pack(side="left", padx=3)
        tk.Button(self.topbar, text="❤️ Wishlist", command=self.show_wishlist,
                  **self.nav_button()).pack(side="left", padx=3)
        tk.Button(self.topbar, text="📦 Orders", command=self.show_orders,
                  **self.nav_button()).pack(side="left", padx=3)
        tk.Button(self.topbar, text="🧠 DSA", command=self.show_dsa,
                  **self.nav_button()).pack(side="left", padx=3)

        tk.Button(self.topbar, text="👨‍💼 Admin", command=self.admin.open_login,
                  bg=PURPLE, fg="white", activebackground="white",
                  activeforeground="black", relief="flat",
                  font=("Arial", 9, "bold"), padx=10, pady=7,
                  cursor="hand2").pack(side="right", padx=8)

        tk.Button(self.topbar, text="🚪 Exit", command=self.exit_app,
                  bg=RED, fg="white", activebackground="white",
                  activeforeground="black", relief="flat",
                  font=("Arial", 9, "bold"), padx=10, pady=7,
                  cursor="hand2").pack(side="right", padx=8)

        self.body = tk.Frame(self.root, bg=BG)
        self.body.pack(fill="both", expand=True)

        self.status = tk.Label(self.root, textvariable=self.status_var,
                               bg="#101010", fg=MUTED, anchor="w",
                               font=("Arial", 9))
        self.status.pack(side="bottom", fill="x", padx=12, pady=3)

    def nav_button(self):
        return {
            "bg": "#101010", "fg": "white",
            "activebackground": "#292929", "activeforeground": NEON,
            "relief": "flat", "font": ("Arial", 9, "bold"),
            "cursor": "hand2", "padx": 8, "pady": 7
        }

    def clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    def set_status(self, text):
        self.status_var.set(text)

    def log_activity(self, text):
        self.activity_log.insert(0, datetime.now().strftime("%H:%M:%S") + "  " + text)
        self.activity_log = self.activity_log[:8]

    def exit_app(self):
        if messagebox.askyesno("Exit", "Exit GAMEZONE?"):
            self.root.destroy()

    #  Home 

    def show_home(self):
        self.clear_body()
        hero = tk.Frame(self.body, bg=BG)
        hero.pack(fill="both", expand=True)

        banner = tk.Frame(hero, bg="#101010", height=150, highlightthickness=1, highlightbackground="#333")
        banner.pack(fill="x", padx=30, pady=(22, 12))
        banner.pack_propagate(False)

        left = tk.Frame(banner, bg="#101010")
        left.pack(side="left", fill="both", expand=True, padx=25)
        self.home_title = tk.Label(left, text="GAMEZONE", bg="#101010", fg=NEON,
                                   font=("Arial", 37, "bold"))
        self.home_title.pack(anchor="w", pady=(17, 0))
        tk.Label(left, text="YOUR NEXT GAME IS WAITING.", bg="#101010", fg=CYAN,
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=2)
        tk.Label(left, text="Shop • Wishlist • Discover • Checkout", bg="#101010", fg=MUTED,
                 font=("Arial", 10)).pack(anchor="w", pady=2)
        self.animate_home_title(0)

        day = self.games[datetime.now().timetuple().tm_yday % len(self.games)]
        deal = 10 + (datetime.now().timetuple().tm_yday % 3) * 5
        deal_box = tk.Frame(banner, bg=PANEL, width=310)
        deal_box.pack(side="right", fill="y", padx=12, pady=12)
        deal_box.pack_propagate(False)
        tk.Label(deal_box, text="🔥 GAME OF THE DAY", bg=PANEL, fg=YELLOW,
                 font=("Arial", 10, "bold")).pack(pady=(10, 2))
        tk.Label(deal_box, text=day.name, bg=PANEL, fg=TEXT,
                 font=("Arial", 16, "bold")).pack()
        tk.Label(deal_box, text=f"⭐ {day.rating:.1f}   •   {deal}% BONUS DEAL", bg=PANEL, fg=GREEN,
                 font=("Arial", 9, "bold")).pack(pady=4)
        tk.Button(deal_box, text="⚡ View Deal", command=lambda: self.show_details(day),
                  bg=GREEN, fg="black", relief="flat", font=("Arial", 9, "bold"),
                  padx=12, pady=5, cursor="hand2").pack(pady=4)

        stats = tk.Frame(hero, bg=BG)
        stats.pack(fill="x", padx=30, pady=5)
        for i, (label, value) in enumerate([
            ("🎮 GAMES", len(self.games)),
            ("❤️ WISHLIST", len(self.wishlist)),
            ("🛒 CART", self.cart.count()),
            ("📦 ORDERS", len(self.orders_history)),
        ]):
            f = tk.Frame(stats, bg=PANEL, highlightthickness=1, highlightbackground="#2d2d2d")
            f.grid(row=0, column=i, sticky="ew", padx=5)
            stats.grid_columnconfigure(i, weight=1)
            tk.Label(f, text=label, bg=PANEL, fg=MUTED, font=("Arial", 9, "bold")).pack(pady=(9, 2))
            tk.Label(f, text=str(value), bg=PANEL, fg=NEON, font=("Arial", 18, "bold")).pack(pady=(0, 9))

        feature_area = tk.Frame(hero, bg=BG)
        feature_area.pack(fill="both", expand=True, padx=30, pady=15)

        left_panel = tk.Frame(feature_area, bg=PANEL)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 7))
        tk.Label(left_panel, text="🏆 TOP PICKS", bg=PANEL, fg=YELLOW,
                 font=("Arial", 14, "bold")).pack(anchor="w", padx=18, pady=(15, 10))
        picks = self.featured_queue.display() or self.top_rated(self.games)[:4]
        for i, g in enumerate(picks[:4], 1):
            row = tk.Frame(left_panel, bg=PANEL2)
            row.pack(fill="x", padx=15, pady=3)
            tk.Label(row, text=f"{i}.", bg=PANEL2, fg=YELLOW, width=4,
                     font=("Arial", 10, "bold")).pack(side="left", pady=8)
            tk.Label(row, text=g.name, bg=PANEL2, fg=TEXT, width=22, anchor="w",
                     font=("Arial", 10, "bold")).pack(side="left")
            tk.Label(row, text=f"⭐ {g.rating:.1f}", bg=PANEL2, fg=YELLOW,
                     font=("Arial", 9, "bold")).pack(side="left", padx=10)
            tk.Button(row, text="OPEN", command=lambda x=g: self.show_details(x),
                      bg=CYAN, fg="black", relief="flat", font=("Arial", 8, "bold"),
                      padx=9, pady=4).pack(side="right", padx=8)

        right_panel = tk.Frame(feature_area, bg=PANEL, width=350)
        right_panel.pack(side="right", fill="y", padx=(7, 0))
        right_panel.pack_propagate(False)
        tk.Label(right_panel, text="🚀 QUICK ACTIONS", bg=PANEL, fg=CYAN,
                 font=("Arial", 14, "bold")).pack(anchor="w", padx=18, pady=(15, 10))
        actions = [
            ("🎮 Explore All Games", self.show_games, NEON),
            ("❤️ Open Wishlist", self.show_wishlist, RED),
            ("🛒 Open Cart", self.show_cart, YELLOW),
            ("🧠 See DSA Live", self.show_dsa, PURPLE),
            ("👨‍💼 Admin Dashboard", self.admin.open_login, CYAN),
        ]
        for text, cmd, color in actions:
            tk.Button(right_panel, text=text, command=cmd, bg=color,
                      fg="black" if color in (NEON, YELLOW, CYAN) else "white",
                      relief="flat", font=("Arial", 10, "bold"),
                      padx=12, pady=8, cursor="hand2").pack(fill="x", padx=18, pady=4)

        self.set_status("Welcome to GAMEZONE • Try Game of the Day or explore the top picks")

    def animate_home_title(self, step):
        if not self.root.winfo_exists():
            return
        colors = [NEON, CYAN, PURPLE, NEON]
        try:
            self.home_title.configure(fg=colors[step % len(colors)])
            self.root.after(500, lambda: self.animate_home_title(step + 1))
        except tk.TclError:
            pass

    # Search / Sort 

    def linear_search(self, games, query):
        q = query.lower().strip()
        if not q:
            return list(games)
        result = []
        for g in games:
            if q in g.name.lower() or q in g.category.lower():
                result.append(g)
        return result

    def bubble_sort(self, data, key, reverse=False):
        a = list(data)
        n = len(a)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                left = key(a[j])
                right = key(a[j + 1])
                condition = left < right if reverse else left > right
                if condition:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swapped = True
            if not swapped:
                break
        return a

    def selection_sort(self, data, key, reverse=False):
        a = list(data)
        n = len(a)
        for i in range(n):
            idx = i
            for j in range(i + 1, n):
                condition = key(a[j]) > key(a[idx]) if reverse else key(a[j]) < key(a[idx])
                if condition:
                    idx = j
            a[i], a[idx] = a[idx], a[i]
        return a

    def insertion_sort(self, data, key, reverse=False):
        a = list(data)
        for i in range(1, len(a)):
            item = a[i]
            j = i - 1
            while j >= 0:
                condition = key(a[j]) < key(item) if reverse else key(a[j]) > key(item)
                if not condition:
                    break
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = item
        return a

    def top_rated(self, games):
        return self.insertion_sort(games, lambda g: g.rating, reverse=True)

    def apply_game_controls(self):
        result = self.linear_search(self.games, self.search_var.get())
        cat = self.category_var.get()
        if cat and cat != "All":
            result = [g for g in result if g.category == cat]

        sort = self.sort_var.get()
        if sort == "Price Low → High":
            result = self.bubble_sort(result, lambda g: g.price)
        elif sort == "Price High → Low":
            result = self.selection_sort(result, lambda g: g.price, reverse=True)
        elif sort == "Rating High → Low":
            result = self.insertion_sort(result, lambda g: g.rating, reverse=True)
        elif sort == "A → Z":
            result = self.bubble_sort(result, lambda g: g.name.lower())

        self.current_games = result
        self.render_game_cards(result)

        if self.search_var.get().strip() and not result:
            self.set_status("❌ Game Not Found")
        elif self.search_var.get().strip() and result:
            self.set_status(f"✅ Game Found • {len(result)} result(s)")
        else:
            self.set_status(f"Showing {len(result)} game(s)")

    def show_games(self):
        self.clear_body()

        head = tk.Frame(self.body, bg=BG)
        head.pack(fill="x", padx=25, pady=(20, 10))
        tk.Label(head, text="🎮 GAME COLLECTION", bg=BG, fg=TEXT,
                 font=("Arial", 25, "bold")).pack(side="left")

        controls = tk.Frame(self.body, bg=PANEL)
        controls.pack(fill="x", padx=25, pady=8)

        tk.Label(controls, text="🔍", bg=PANEL, fg=TEXT,
                 font=("Arial", 13)).pack(side="left", padx=(15, 4))
        self.search_entry = tk.Entry(controls, textvariable=self.search_var,
                                     bg="#292929", fg=TEXT,
                                     insertbackground=TEXT, relief="flat",
                                     font=("Arial", 10), width=25)
        self.search_entry.pack(side="left", ipady=7, padx=4)
        tk.Button(controls, text="SEARCH", command=self.apply_game_controls,
                  bg=NEON, fg="black", relief="flat",
                  font=("Arial", 9, "bold"), padx=12, pady=6).pack(side="left", padx=4)

        categories = ["All"] + self.unique_categories()
        combo = ttk.Combobox(controls, textvariable=self.category_var,
                             values=categories, state="readonly", width=15)
        combo.pack(side="left", padx=10)
        combo.bind("<<ComboboxSelected>>", lambda e: self.apply_game_controls())

        sorts = ["Default", "Price Low → High", "Price High → Low",
                 "Rating High → Low", "A → Z"]
        combo2 = ttk.Combobox(controls, textvariable=self.sort_var,
                              values=sorts, state="readonly", width=18)
        combo2.pack(side="left", padx=5)
        combo2.bind("<<ComboboxSelected>>", lambda e: self.apply_game_controls())

        tk.Button(controls, text="Reset", command=self.reset_game_controls,
                  bg=PANEL2, fg=TEXT, relief="flat",
                  font=("Arial", 9, "bold"), padx=12, pady=6).pack(side="right", padx=12)

        self.canvas = tk.Canvas(self.body, bg=BG, highlightthickness=0)
        self.scroll = tk.Scrollbar(self.body, orient="vertical", command=self.canvas.yview)
        self.cards_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(25, 0), pady=8)
        self.scroll.pack(side="right", fill="y", padx=(0, 15), pady=8)

        self.cards_frame.bind("<Configure>",
                              lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.resize_cards)
        self.canvas.bind_all("<MouseWheel>", self.mousewheel)

        self.apply_game_controls()

    def resize_cards(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
        except:
            pass

    def reset_game_controls(self):
        self.search_var.set("")
        self.category_var.set("All")
        self.sort_var.set("Default")
        self.apply_game_controls()

    def unique_categories(self):
        cats = []
        for g in self.games:
            if g.category not in cats:
                cats.append(g.category)
        return cats

    def render_game_cards(self, games):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        if not games:
            tk.Label(self.cards_frame, text="❌ Game Not Found",
                     bg=BG, fg=RED, font=("Arial", 20, "bold")).pack(pady=100)
            return

        for i, g in enumerate(games):
            row = i // 3
            col = i % 3
            self.cards_frame.grid_columnconfigure(col, weight=1)
            self.game_card(self.cards_frame, g, row, col)

    def game_card(self, parent, game, row, col):
        card = tk.Frame(parent, bg=CARD, width=300, height=245,
                        highlightthickness=1, highlightbackground="#333")
        card.grid(row=row, column=col, padx=9, pady=9, sticky="nsew")
        card.grid_propagate(False)

        tk.Label(card, text="🎮", bg=CARD, fg=NEON,
                 font=("Arial", 25)).pack(pady=(13, 0))
        tk.Label(card, text=game.name, bg=CARD, fg=TEXT,
                 font=("Arial", 14, "bold")).pack(pady=3)
        tk.Label(card, text=f"📂 {game.category}   ⭐ {game.rating:.1f}",
                 bg=CARD, fg=YELLOW, font=("Arial", 9, "bold")).pack()
        price = "FREE" if game.price == 0 else f"₹{game.price:.0f}"
        tk.Label(card, text=f"💰 {price}", bg=CARD, fg=NEON,
                 font=("Arial", 12, "bold")).pack(pady=4)

        b = tk.Frame(card, bg=CARD)
        b.pack(pady=7)
        self.small_button(b, "View Details", lambda x=game: self.show_details(x), CYAN).pack(side="left", padx=2)
        self.small_button(b, "Cart", lambda x=game: self.add_to_cart(x), NEON).pack(side="left", padx=2)
        self.small_button(b, "♥", lambda x=game: self.toggle_wishlist(x), RED).pack(side="left", padx=2)
        self.small_button(b, "Buy", lambda x=game: self.buy_now(x), PURPLE).pack(side="left", padx=2)

        for widget in [card]:
            widget.bind("<Enter>", lambda e, c=card: self.hover_card(c, True))
            widget.bind("<Leave>", lambda e, c=card: self.hover_card(c, False))

    def small_button(self, parent, text, command, color):
        return tk.Button(parent, text=text, command=command, bg=color,
                         fg="black" if color != RED and color != PURPLE else "white",
                         activebackground="white", relief="flat",
                         font=("Arial", 8, "bold"), padx=7, pady=5,
                         cursor="hand2")

    def hover_card(self, card, entering):
        card.configure(highlightbackground=NEON if entering else "#333")

    # ------------------------- Details -------------------------

    def show_details(self, game):
        self.recent.push(game)
        self.log_activity(f"Viewed {game.name}")
        self.clear_body()

        frame = tk.Frame(self.body, bg=BG)
        frame.pack(fill="both", expand=True, padx=60, pady=45)

        tk.Label(frame, text="🎮", bg=BG, fg=NEON,
                 font=("Arial", 45)).pack()
        tk.Label(frame, text=game.name, bg=BG, fg=TEXT,
                 font=("Arial", 32, "bold")).pack(pady=5)
        tk.Label(frame, text=f"📂 {game.category}    ⭐ {game.rating:.1f}    "
                             f"💰 {'FREE' if game.price == 0 else '₹' + format(game.price, '.0f')}",
                 bg=BG, fg=YELLOW, font=("Arial", 13, "bold")).pack(pady=10)

        desc = tk.Frame(frame, bg=PANEL)
        desc.pack(fill="x", padx=80, pady=20)
        tk.Label(desc, text="DESCRIPTION", bg=PANEL, fg=CYAN,
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(18, 5))
        tk.Label(desc, text=game.description, bg=PANEL, fg=TEXT,
                 font=("Arial", 12), wraplength=750, justify="left").pack(
                     anchor="w", padx=20, pady=(0, 20))

        buttons = tk.Frame(frame, bg=BG)
        buttons.pack(pady=20)
        tk.Button(buttons, text="🛒 Add to Cart", command=lambda: self.add_to_cart(game),
                  bg=NEON, fg="black", relief="flat", font=("Arial", 11, "bold"),
                  padx=22, pady=10).pack(side="left", padx=6)
        tk.Button(buttons, text="❤️ Wishlist", command=lambda: self.toggle_wishlist(game),
                  bg=RED, fg="white", relief="flat", font=("Arial", 11, "bold"),
                  padx=22, pady=10).pack(side="left", padx=6)
        tk.Button(buttons, text="⚡ Buy Now", command=lambda: self.buy_now(game),
                  bg=PURPLE, fg="white", relief="flat", font=("Arial", 11, "bold"),
                  padx=22, pady=10).pack(side="left", padx=6)
        tk.Button(buttons, text="← Back", command=self.show_games,
                  bg=PANEL2, fg=TEXT, relief="flat", font=("Arial", 11, "bold"),
                  padx=22, pady=10).pack(side="left", padx=6)

        self.set_status(f"Recently Viewed Stack: {game.name} pushed")

    #  Cart 

    def add_to_cart(self, game):
        if self.cart.add(game):
            self.log_activity(f"Added {game.name} to cart")
            messagebox.showinfo("Cart", f"🛒 {game.name} added to cart.")
            self.set_status(f"Cart Linked List: {self.cart.count()} node(s)")
        else:
            messagebox.showinfo("Cart", f"{game.name} is already in the cart.")

    def remove_from_cart(self, game):
        if self.cart.remove(game.game_id):
            messagebox.showinfo("Cart", f"{game.name} removed.")
        else:
            messagebox.showwarning("Cart", "Game is not in the cart.")
        self.show_cart()

    def clear_cart(self):
        if self.cart.count() == 0:
            messagebox.showinfo("Cart", "Cart is already empty.")
            return
        if messagebox.askyesno("Clear Cart", "Remove all games from cart?"):
            self.cart.clear()
            self.show_cart()

    def show_cart(self):
        self.clear_body()
        tk.Label(self.body, text="🛒 SHOPPING CART", bg=BG, fg=TEXT,
                 font=("Arial", 27, "bold")).pack(anchor="w", padx=35, pady=(25, 10))

        items = self.cart.display()
        if not items:
            box = tk.Frame(self.body, bg=PANEL)
            box.pack(fill="both", expand=True, padx=35, pady=20)
            tk.Label(box, text="🛒", bg=PANEL, fg=MUTED,
                     font=("Arial", 50)).pack(pady=(100, 10))
            tk.Label(box, text="Your cart is empty", bg=PANEL, fg=TEXT,
                     font=("Arial", 18, "bold")).pack()
            tk.Button(box, text="🎮 Continue Shopping", command=self.show_games,
                      bg=NEON, fg="black", relief="flat",
                      font=("Arial", 11, "bold"), padx=25, pady=10).pack(pady=20)
            return

        area = tk.Frame(self.body, bg=BG)
        area.pack(fill="both", expand=True, padx=35)

        left = tk.Frame(area, bg=PANEL)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="GAME                         PRICE",
                 bg=PANEL, fg=MUTED, font=("Arial", 10, "bold")).pack(
                     anchor="w", padx=20, pady=15)
        for g in items:
            row = tk.Frame(left, bg=PANEL2)
            row.pack(fill="x", padx=12, pady=4)
            tk.Label(row, text=f"🎮 {g.name}", bg=PANEL2, fg=TEXT,
                     font=("Arial", 11, "bold"), width=28, anchor="w").pack(
                         side="left", padx=10, pady=10)
            tk.Label(row, text=f"₹{g.price:.0f}", bg=PANEL2, fg=NEON,
                     font=("Arial", 11, "bold"), width=12).pack(side="left")
            tk.Button(row, text="Remove", command=lambda x=g: self.remove_from_cart(x),
                      bg=RED, fg="white", relief="flat",
                      font=("Arial", 8, "bold"), padx=10, pady=5).pack(side="right", padx=10)

        right = tk.Frame(area, bg=PANEL, width=300)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        subtotal = self.cart.calculate_total()
        discount = 100 if subtotal >= 1500 else 0
        total = max(0, subtotal - discount)

        tk.Label(right, text="ORDER SUMMARY", bg=PANEL, fg=CYAN,
                 font=("Arial", 14, "bold")).pack(anchor="w", padx=20, pady=25)
        self.summary_line(right, "Items", str(len(items)))
        self.summary_line(right, "Subtotal", f"₹{subtotal:.0f}")
        self.summary_line(right, "Discount", f"- ₹{discount:.0f}")
        tk.Frame(right, bg="#333", height=1).pack(fill="x", padx=20, pady=15)
        self.summary_line(right, "Total", f"₹{total:.0f}", big=True)

        tk.Button(right, text="💳 CHECKOUT", command=self.checkout,
                  bg=NEON, fg="black", relief="flat",
                  font=("Arial", 11, "bold"), padx=25, pady=10).pack(pady=18)
        tk.Button(right, text="🗑 Clear Cart", command=self.clear_cart,
                  bg=RED, fg="white", relief="flat",
                  font=("Arial", 10, "bold"), padx=20, pady=8).pack()

    def summary_line(self, parent, name, value, big=False):
        f = tk.Frame(parent, bg=PANEL)
        f.pack(fill="x", padx=20, pady=5)
        tk.Label(f, text=name, bg=PANEL, fg=MUTED if not big else TEXT,
                 font=("Arial", 10 if not big else 13,
                       "bold" if big else "normal")).pack(side="left")
        tk.Label(f, text=value, bg=PANEL, fg=NEON,
                 font=("Arial", 10 if not big else 14, "bold")).pack(side="right")

    # Wishlist 

    def toggle_wishlist(self, game):
        if game.game_id in self.wishlist:
            self.wishlist.remove(game.game_id)
            messagebox.showinfo("Wishlist", f"{game.name} removed from wishlist.")
        else:
            self.wishlist.add(game.game_id)
            messagebox.showinfo("Wishlist", f"❤️ {game.name} added to wishlist.")
        self.set_status(f"Wishlist contains {len(self.wishlist)} game(s)")

    def show_wishlist(self):
        self.clear_body()
        tk.Label(self.body, text="❤️ WISHLIST", bg=BG, fg=TEXT,
                 font=("Arial", 27, "bold")).pack(anchor="w", padx=35, pady=(25, 10))

        games = [self.game_table[i] for i in self.wishlist if i in self.game_table]
        if not games:
            tk.Label(self.body, text="❤️ Your wishlist is empty.",
                     bg=BG, fg=MUTED, font=("Arial", 16)).pack(pady=100)
            return

        frame = tk.Frame(self.body, bg=BG)
        frame.pack(fill="both", expand=True, padx=35)
        for i, g in enumerate(games):
            row = tk.Frame(frame, bg=PANEL)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=f"❤️ {g.name}", bg=PANEL, fg=TEXT,
                     font=("Arial", 12, "bold"), width=30, anchor="w").pack(
                         side="left", padx=15, pady=12)
            tk.Label(row, text=f"₹{g.price:.0f}", bg=PANEL, fg=NEON,
                     font=("Arial", 11, "bold")).pack(side="left", padx=20)
            tk.Button(row, text="🛒 Move to Cart", command=lambda x=g: self.move_to_cart(x),
                      bg=NEON, fg="black", relief="flat",
                      font=("Arial", 9, "bold"), padx=12, pady=6).pack(side="right", padx=5)
            tk.Button(row, text="🗑 Remove", command=lambda x=g: self.remove_wishlist(x),
                      bg=RED, fg="white", relief="flat",
                      font=("Arial", 9, "bold"), padx=12, pady=6).pack(side="right", padx=5)

    def move_to_cart(self, game):
        if self.cart.add(game):
            self.wishlist.discard(game.game_id)
            messagebox.showinfo("Wishlist", f"{game.name} moved to cart.")
        else:
            messagebox.showinfo("Cart", f"{game.name} is already in cart.")
        self.show_wishlist()

    def remove_wishlist(self, game):
        self.wishlist.discard(game.game_id)
        self.show_wishlist()

    # Checkout

    def checkout(self):
        items = self.cart.display()
        if not items:
            messagebox.showwarning("Checkout", "Cannot checkout with an empty cart.")
            return

        win = tk.Toplevel(self.root)
        win.title("GAMEZONE - Checkout")
        win.geometry("650x680")
        win.configure(bg=BG)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="💳 CHECKOUT", bg=BG, fg=NEON,
                 font=("Arial", 24, "bold")).pack(pady=20)

        form = tk.Frame(win, bg=PANEL)
        form.pack(fill="x", padx=35)

        entries = {}
        for label in ["Name", "Address", "Phone"]:
            tk.Label(form, text=label, bg=PANEL, fg=TEXT,
                     font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(12, 4))
            e = tk.Entry(form, bg="#292929", fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=("Arial", 10))
            e.pack(fill="x", padx=20, ipady=7)
            entries[label] = e

        tk.Label(form, text="Payment Method", bg=PANEL, fg=CYAN,
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(16, 5))
        payment = tk.StringVar(value="Cash on Delivery")
        for option in ["Cash on Delivery", "UPI", "Card"]:
            tk.Radiobutton(form, text=option, variable=payment, value=option,
                           bg=PANEL, fg=TEXT, selectcolor="#292929",
                           activebackground=PANEL, activeforeground=NEON,
                           font=("Arial", 10)).pack(anchor="w", padx=30, pady=2)

        subtotal = self.cart.calculate_total()
        discount = 100 if subtotal >= 1500 else 0
        total = max(0, subtotal - discount)

        tk.Label(win, text=f"Order Total: ₹{total:.0f}",
                 bg=BG, fg=YELLOW, font=("Arial", 15, "bold")).pack(pady=18)

        def place():
            name = entries["Name"].get().strip()
            address = entries["Address"].get().strip()
            phone = entries["Phone"].get().strip()
            if not name or not address or not phone:
                messagebox.showerror("Invalid Details", "Please enter Name, Address and Phone.")
                return
            if not phone.isdigit() or len(phone) < 10:
                messagebox.showerror("Invalid Phone", "Enter a valid demo phone number.")
                return

            oid = "GZ" + str(self.order_number)
            self.order_number += 1
            order = {
                "id": oid,
                "customer": name,
                "address": address,
                "phone": phone,
                "items": [g.name for g in items],
                "game_ids": [g.game_id for g in items],
                "total": total,
                "payment": payment.get(),
                "status": "Pending",
                "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            }
            self.orders_history.append(order)
            self.order_queue.enqueue(order)
            self.log_activity(f"Order {oid} created")
            self.cart.clear()
            win.destroy()
            self.order_success(order)

        tk.Button(win, text="PLACE ORDER", command=place,
                  bg=NEON, fg="black", relief="flat",
                  font=("Arial", 12, "bold"), padx=40, pady=11).pack(pady=5)

    def buy_now(self, game):
        if not self.cart.contains(game.game_id):
            self.cart.add(game)
        self.checkout()

    def order_success(self, order):
        win = tk.Toplevel(self.root)
        win.title("Order Success")
        win.geometry("600x430")
        win.configure(bg=BG)
        win.transient(self.root)

        label = tk.Label(win, text="🎉", bg=BG, fg=NEON, font=("Arial", 55))
        label.pack(pady=(35, 5))
        title = tk.Label(win, text="ORDER SUCCESS!", bg=BG, fg=NEON,
                         font=("Arial", 26, "bold"))
        title.pack()
        tk.Label(win, text=f"Order ID: {order['id']}", bg=BG, fg=YELLOW,
                 font=("Arial", 14, "bold")).pack(pady=12)
        tk.Label(win, text="Your order has been placed successfully!",
                 bg=BG, fg=TEXT, font=("Arial", 12)).pack()
        tk.Label(win, text=f"Total: ₹{order['total']:.0f}",
                 bg=BG, fg=MUTED, font=("Arial", 11)).pack(pady=5)

        def pulse(n=0):
            if not win.winfo_exists():
                return
            if n < 8:
                title.configure(fg=NEON if n % 2 == 0 else CYAN)
                win.after(180, lambda: pulse(n + 1))
        pulse()
        tk.Button(win, text="VIEW ORDERS", command=lambda: (win.destroy(), self.show_orders()),
                  bg=CYAN, fg="black", relief="flat",
                  font=("Arial", 10, "bold"), padx=25, pady=9).pack(pady=20)

        self.set_status(f"🎉 {order['id']} placed • Queue updated")

    # Orders 

    def show_orders(self):
        self.clear_body()
        tk.Label(self.body, text="📦 ORDERS", bg=BG, fg=TEXT,
                 font=("Arial", 27, "bold")).pack(anchor="w", padx=35, pady=(25, 10))

        if not self.orders_history:
            tk.Label(self.body, text="No orders placed yet.",
                     bg=BG, fg=MUTED, font=("Arial", 16)).pack(pady=100)
            return

        tree = ttk.Treeview(self.body,
                            columns=("id", "customer", "items", "total", "status"),
                            show="headings")
        for c, h, w in [
            ("id", "Order ID", 100), ("customer", "Customer", 160),
            ("items", "Items", 360), ("total", "Total", 110),
            ("status", "Status", 130)
        ]:
            tree.heading(c, text=h)
            tree.column(c, width=w, anchor="center")
        tree.pack(fill="both", expand=True, padx=35, pady=15)

        for o in self.orders_history:
            tree.insert("", "end", values=(o["id"], o["customer"],
                                           ", ".join(o["items"]),
                                           f"₹{o['total']:.0f}", o["status"]))

        tk.Button(self.body, text="🧠 View Queue / DSA",
                  command=self.show_dsa, bg=PURPLE, fg="white",
                  relief="flat", font=("Arial", 10, "bold"),
                  padx=20, pady=8).pack(pady=10)

    # DSA Page 

    def show_dsa(self):
        self.clear_body()
        tk.Label(self.body, text="🧠 DSA BEHIND GAMEZONE", bg=BG, fg=NEON,
                 font=("Arial", 27, "bold")).pack(anchor="w", padx=30, pady=(22, 5))
        tk.Label(self.body, text="Live visualization of the actual structures powering the application",
                 bg=BG, fg=MUTED, font=("Arial", 10)).pack(anchor="w", padx=32, pady=(0, 12))

        canvas = tk.Canvas(self.body, bg=BG, highlightthickness=0)
        scroll = tk.Scrollbar(self.body, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True, padx=(30, 0))
        scroll.pack(side="right", fill="y", padx=(0, 15))

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.dsa_box(inner, "📦 ARRAY / LIST — GAME COLLECTION",
                     [g.name for g in self.games], "Array/List stores the main game collection.")

        self.dsa_box(inner, "🔗 LINKED LIST — SHOPPING CART",
                     [g.name for g in self.cart.display()] + ["NULL"],
                     "Cart nodes are connected through Node.next.")

        self.dsa_box(inner, "🥞 STACK — RECENTLY VIEWED",
                     ["TOP"] + [g.name for g in self.recent.display()],
                     "LIFO: the latest viewed game is shown first.")

        q = self.order_queue.display()
        qlabels = ["FRONT"] + [o["id"] for o in q] + (["REAR"] if q else [])
        self.dsa_box(inner, "🚶 QUEUE — ORDER PROCESSING",
                     qlabels, "FIFO: first order in is the first order processed.")

        self.dsa_box(inner, "🏆 PRIORITY QUEUE / HEAP — FEATURED",
                     [f"{g.name} ⭐ {g.rating:.1f}" for g in self.featured_queue.display()],
                     "Higher rating gets higher priority.")

        self.dsa_box(inner, "🔑 HASH TABLE — GAME ID LOOKUP",
                     [f"{gid} → {g.name}" for gid, g in self.game_table.items()],
                     "Dictionary gives fast Game ID lookup.")

        category_lines = []
        for cat, ids in self.category_index.items():
            names = []
            for gid in ids[:5]:
                if gid in self.game_table:
                    names.append(self.game_table[gid].name)
            category_lines.append(f"{cat}: " + ", ".join(names))
        self.dsa_box(inner, "🗂️ CATEGORY INDEX — DICTIONARY",
                     category_lines, "Dictionary groups Game IDs by category for fast category filtering.")

        self.dsa_box(inner, "⚡ LIVE ACTIVITY",
                     self.activity_log if self.activity_log else ["No activity yet"],
                     "Recent customer actions are kept in a small application activity list.")

        self.dsa_box(inner, "🔍 SEARCHING — LINEAR SEARCH",
                     ["Query → compare games one by one → matching result"],
                     "Used by the Game Search box.")

        self.dsa_box(inner, "↕ SORTING ALGORITHMS",
                     ["Bubble Sort", "Selection Sort", "Insertion Sort"],
                     "Used for price, rating and name sorting.")

    def dsa_box(self, parent, heading, values, explanation):
        box = tk.Frame(parent, bg=PANEL)
        box.pack(fill="x", pady=7, padx=5)
        tk.Label(box, text=heading, bg=PANEL, fg=CYAN,
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=18, pady=(13, 7))
        if not values:
            values = ["EMPTY"]
        row = tk.Frame(box, bg=PANEL)
        row.pack(fill="x", padx=15, pady=5)
        for i, value in enumerate(values[:30]):
            tk.Label(row, text=f"[ {value} ]", bg=PANEL2, fg=TEXT,
                     font=("Arial", 9, "bold"), padx=8, pady=7).pack(side="left", padx=2, pady=2)
        tk.Label(box, text=explanation, bg=PANEL, fg=MUTED,
                 font=("Arial", 9)).pack(anchor="w", padx=18, pady=(4, 13))

    # Run 

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GameShop()
    app.run()
