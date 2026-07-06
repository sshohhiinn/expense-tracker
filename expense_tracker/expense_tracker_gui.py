import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import datetime

# ── Config ──────────────────────────────────────────────────────────
FILE       = "expenses.csv"
FIELDS     = ["ID", "Date", "Category", "Description", "Amount"]
CATEGORIES = ["Food", "Transport", "Shopping", "Bills",
              "Health", "Entertainment", "Education", "Other"]

# ── Colors ──────────────────────────────────────────────────────────
BG        = "#F0EFEA"
CARD_BG   = "#FFFFFF"
SIDE_BG   = "#1E1E2E"
SIDE_FG   = "#CDD6F4"
ACCENT    = "#534AB7"
ACCENT_LT = "#EEEDFE"
ACCENT_DK = "#3C3489"
TEXT_PRI  = "#1A1A18"
TEXT_SEC  = "#6B6B67"
TEXT_TER  = "#9B9B96"
BORDER    = "#D0D0CC"
GREEN     = "#0F6E56"
RED       = "#A32D2D"
RED_BG    = "#FEECEC"

CAT_COLORS = {
    "Food":          {"bg": "#9FE1CB", "fg": "#085041"},
    "Transport":     {"bg": "#B5D4F4", "fg": "#0C447C"},
    "Shopping":      {"bg": "#F4C0D1", "fg": "#72243E"},
    "Bills":         {"bg": "#FAC775", "fg": "#633806"},
    "Health":        {"bg": "#F5C4B3", "fg": "#712B13"},
    "Entertainment": {"bg": "#CECBF6", "fg": "#26215C"},
    "Education":     {"bg": "#C0DD97", "fg": "#27500A"},
    "Other":         {"bg": "#D3D1C7", "fg": "#444441"},
}

# ── CSV Helpers ──────────────────────────────────────────────────────
def init_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()

def load():
    init_file()
    with open(FILE, "r", newline="") as f:
        return list(csv.DictReader(f))

def save(expenses):
    with open(FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(expenses)

def next_id(expenses):
    return max((int(e["ID"]) for e in expenses), default=0) + 1

# ── App ──────────────────────────────────────────────────────────────
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("900x620")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.minsize(750, 500)

        self.expenses     = load()
        self.filter_cat   = tk.StringVar(value="All")
        self.filter_month = tk.StringVar(value="All")
        self.search_var   = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.render())

        self._styles()
        self._build_ui()
        self.render()
        self.update_stats()

    # ── Styles ──────────────────────────────────────────────────────
    def _styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TCombobox",
            fieldbackground="#F5F5F4", background="#F5F5F4",
            foreground=TEXT_PRI, bordercolor=BORDER,
            arrowcolor=TEXT_SEC, relief="flat", padding=6)
        s.map("TCombobox",
            fieldbackground=[("readonly","#F5F5F4")],
            foreground=[("readonly", TEXT_PRI)])
        s.configure("Vertical.TScrollbar",
            background=BG, troughcolor=BG,
            bordercolor=BG, arrowcolor=TEXT_SEC, relief="flat")

    # ── UI ───────────────────────────────────────────────────────────
    def _build_ui(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Sidebar
        side = tk.Frame(self.root, bg=SIDE_BG, width=210)
        side.grid(row=0, column=0, sticky="nsew")
        side.grid_propagate(False)
        self._build_sidebar(side)

        # Main
        main = tk.Frame(self.root, bg=BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)
        self._build_main(main)

    # ── Sidebar ──────────────────────────────────────────────────────
    def _build_sidebar(self, p):
        tk.Label(p, text="💰  Expense Tracker",
                 font=("Helvetica", 14, "bold"),
                 bg=SIDE_BG, fg=SIDE_FG).pack(anchor="w", padx=18, pady=(22,2))
        tk.Label(p, text="Track your spending",
                 font=("Helvetica", 10), bg=SIDE_BG, fg="#6C7086").pack(anchor="w", padx=18, pady=(0,12))

        tk.Frame(p, bg="#313244", height=1).pack(fill="x", padx=14, pady=4)

        # Stats
        sf = tk.Frame(p, bg=SIDE_BG)
        sf.pack(fill="x", padx=12, pady=6)
        self._stat(sf, "Total Spent",   "₹0.00",  "#CDD6F4", "s_total")
        self._stat(sf, "This Month",    "₹0.00",  "#A6E3A1", "s_month")
        self._stat(sf, "Records",       "0",       "#F38BA8", "s_count")
        self._stat(sf, "Avg per Entry", "₹0.00",  "#FAB387", "s_avg")

        tk.Frame(p, bg="#313244", height=1).pack(fill="x", padx=14, pady=8)

        # Category filter
        tk.Label(p, text="CATEGORY", font=("Helvetica", 9, "bold"),
                 bg=SIDE_BG, fg="#6C7086").pack(anchor="w", padx=18, pady=(0,4))
        for cat in ["All"] + CATEGORIES:
            self._side_btn(p, cat, self.filter_cat, self.render)

        tk.Frame(p, bg="#313244", height=1).pack(fill="x", padx=14, pady=8)

        # Export button
        tk.Button(p, text="📤  Export CSV",
                  font=("Helvetica", 10), relief="flat",
                  bg="#313244", fg=SIDE_FG, cursor="hand2",
                  activebackground=ACCENT, activeforeground="white",
                  command=self.export_csv).pack(fill="x", padx=14, pady=4, ipady=6)

    def _stat(self, p, label, val, color, attr):
        f = tk.Frame(p, bg="#313244")
        f.pack(fill="x", pady=3)
        tk.Label(f, text=label, font=("Helvetica", 9),
                 bg="#313244", fg="#6C7086").pack(side="left", padx=10, pady=6)
        lbl = tk.Label(f, text=val, font=("Helvetica", 10, "bold"),
                       bg="#313244", fg=color)
        lbl.pack(side="right", padx=10)
        setattr(self, attr, lbl)

    def _side_btn(self, p, text, var, cmd):
        f = tk.Frame(p, bg=SIDE_BG, cursor="hand2")
        f.pack(fill="x", padx=12, pady=1)
        lbl = tk.Label(f, text=text, font=("Helvetica", 10),
                       bg=SIDE_BG, fg="#6C7086", anchor="w", padx=8, pady=4)
        lbl.pack(fill="x")
        def click():
            var.set(text); cmd()
        lbl.bind("<Button-1>", lambda e: click())
        f.bind("<Button-1>",   lambda e: click())
        def on_enter(e):
            if var.get() != text: lbl.config(fg=SIDE_FG)
        def on_leave(e):
            if var.get() != text: lbl.config(fg="#6C7086")
        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)

    # ── Main Area ────────────────────────────────────────────────────
    def _build_main(self, p):
        # Top bar
        top = tk.Frame(p, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
        top.columnconfigure(0, weight=1)

        tk.Label(top, text="My Expenses",
                 font=("Helvetica", 18, "bold"),
                 bg=BG, fg=TEXT_PRI).grid(row=0, column=0, sticky="w")

        # Search
        sf = tk.Frame(top, bg="#F5F5F4",
                      highlightbackground=BORDER, highlightthickness=1)
        sf.grid(row=0, column=1, padx=(0,10))
        tk.Label(sf, text="🔍", bg="#F5F5F4", fg=TEXT_SEC,
                 font=("Helvetica",11)).pack(side="left", padx=(8,4))
        tk.Entry(sf, textvariable=self.search_var,
                 font=("Helvetica",11), relief="flat",
                 bg="#F5F5F4", fg=TEXT_PRI, width=16,
                 insertbackground=TEXT_PRI).pack(side="left", ipady=6, padx=(0,8))

        # Add button
        tk.Button(top, text="＋  Add Expense",
                  font=("Helvetica",11,"bold"),
                  bg=ACCENT, fg="white", relief="flat",
                  padx=14, pady=6, cursor="hand2",
                  activebackground=ACCENT_DK,
                  command=self.open_add).grid(row=0, column=2)

        # Table area
        tbl_frame = tk.Frame(p, bg=BG)
        tbl_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))
        tbl_frame.columnconfigure(0, weight=1)
        tbl_frame.rowconfigure(0, weight=1)

        # Canvas scroll
        self.canvas = tk.Canvas(tbl_frame, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        self.inner = tk.Frame(self.canvas, bg=BG)
        self.win   = self.canvas.create_window((0,0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
            lambda e: self.canvas.itemconfig(self.win, width=e.width))
        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ── Render ───────────────────────────────────────────────────────
    def render(self):
        for w in self.inner.winfo_children():
            w.destroy()

        rows = self._filtered()

        if not rows:
            tk.Label(self.inner, text="No expenses found  💸",
                     font=("Helvetica",14), bg=BG,
                     fg=TEXT_TER).pack(pady=60)
            self.update_stats()
            return

        # Header row
        hdr = tk.Frame(self.inner, bg=BG)
        hdr.pack(fill="x", pady=(4,2))
        for txt, w in [("ID",40),("Date",90),("Category",110),
                       ("Description",200),("Amount",80),("",70)]:
            tk.Label(hdr, text=txt, font=("Helvetica",9,"bold"),
                     bg=BG, fg=TEXT_SEC, width=w//7,
                     anchor="w").pack(side="left", padx=4)

        tk.Frame(self.inner, bg=BORDER, height=1).pack(fill="x", pady=2)

        total = 0
        for e in rows:
            amt = float(e["Amount"])
            total += amt
            self._expense_row(e, amt)

        # Total row
        tk.Frame(self.inner, bg=BORDER, height=1).pack(fill="x", pady=6)
        trow = tk.Frame(self.inner, bg="#F5F5F4")
        trow.pack(fill="x", pady=2, ipady=6)
        tk.Label(trow, text=f"  Total  ({len(rows)} records)",
                 font=("Helvetica",11,"bold"),
                 bg="#F5F5F4", fg=TEXT_PRI).pack(side="left", padx=12)
        tk.Label(trow, text=f"₹{total:.2f}",
                 font=("Helvetica",12,"bold"),
                 bg="#F5F5F4", fg=GREEN).pack(side="right", padx=20)

        self.update_stats()

    def _expense_row(self, e, amt):
        c   = CAT_COLORS.get(e["Category"], CAT_COLORS["Other"])
        row = tk.Frame(self.inner, bg=CARD_BG,
                       highlightbackground="#E8E8E4", highlightthickness=1)
        row.pack(fill="x", pady=2, ipady=4)

        # ID
        tk.Label(row, text=f"#{e['ID']}",
                 font=("Helvetica",10), bg=CARD_BG,
                 fg=TEXT_TER, width=4).pack(side="left", padx=(10,4))
        # Date
        tk.Label(row, text=e["Date"],
                 font=("Helvetica",10), bg=CARD_BG,
                 fg=TEXT_SEC, width=10).pack(side="left", padx=4)
        # Category badge
        tk.Label(row, text=e["Category"],
                 font=("Helvetica",9,"bold"),
                 bg=c["bg"], fg=c["fg"],
                 padx=8, pady=2).pack(side="left", padx=6)
        # Description
        tk.Label(row, text=e["Description"],
                 font=("Helvetica",10), bg=CARD_BG,
                 fg=TEXT_PRI, anchor="w", width=22).pack(side="left", padx=4)
        # Amount
        tk.Label(row, text=f"₹{amt:.2f}",
                 font=("Helvetica",11,"bold"),
                 bg=CARD_BG, fg=GREEN).pack(side="left", padx=10)

        # Buttons
        tk.Button(row, text="✏️", relief="flat", bg=CARD_BG,
                  font=("Helvetica",12), cursor="hand2",
                  activebackground=ACCENT_LT,
                  command=lambda ex=e: self.open_edit(ex)).pack(side="right", padx=4)
        tk.Button(row, text="🗑", relief="flat", bg=CARD_BG,
                  font=("Helvetica",12), cursor="hand2",
                  activebackground=RED_BG,
                  command=lambda ex=e: self.delete(ex)).pack(side="right", padx=4)

    # ── Filter ───────────────────────────────────────────────────────
    def _filtered(self):
        rows = self.expenses[:]
        fc   = self.filter_cat.get()
        kw   = self.search_var.get().lower()
        if fc != "All":
            rows = [e for e in rows if e["Category"] == fc]
        if kw:
            rows = [e for e in rows
                    if kw in e["Description"].lower()
                    or kw in e["Category"].lower()
                    or kw in e["Date"]]
        return rows

    # ── Stats ─────────────────────────────────────────────────────────
    def update_stats(self):
        ym    = datetime.date.today().strftime("%Y-%m")
        total = sum(float(e["Amount"]) for e in self.expenses)
        month = sum(float(e["Amount"]) for e in self.expenses
                    if e["Date"].startswith(ym))
        count = len(self.expenses)
        avg   = total / count if count else 0
        self.s_total.config(text=f"₹{total:.2f}")
        self.s_month.config(text=f"₹{month:.2f}")
        self.s_count.config(text=str(count))
        self.s_avg.config(text=f"₹{avg:.2f}")

    # ── Actions ───────────────────────────────────────────────────────
    def delete(self, e):
        if messagebox.askyesno("Delete",
                f"Delete expense '{e['Description']}'?"):
            self.expenses = [ex for ex in self.expenses
                             if str(ex["ID"]) != str(e["ID"])]
            save(self.expenses)
            self.render()

    def export_csv(self):
        if not self.expenses:
            messagebox.showinfo("Export", "No expenses to export!")
            return
        out = f"export_{datetime.date.today()}.csv"
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(self.expenses)
        messagebox.showinfo("Exported", f"Saved as '{out}'")

    # ── Dialog ────────────────────────────────────────────────────────
    def open_add(self):
        self._dialog()

    def open_edit(self, e):
        self._dialog(e)

    def _dialog(self, expense=None):
        dlg = tk.Toplevel(self.root)
        dlg.title("Edit Expense" if expense else "Add Expense")
        dlg.geometry("420x380")
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()
        dlg.transient(self.root)

        tk.Label(dlg, text="Edit Expense" if expense else "New Expense",
                 font=("Helvetica",16,"bold"),
                 bg=BG, fg=TEXT_PRI).pack(anchor="w", padx=24, pady=(20,14))

        card = tk.Frame(dlg, bg=CARD_BG,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", padx=20)

        def field(label, widget_fn):
            f = tk.Frame(card, bg=CARD_BG)
            f.pack(fill="x", padx=16, pady=7)
            tk.Label(f, text=label, font=("Helvetica",9,"bold"),
                     bg=CARD_BG, fg=TEXT_SEC,
                     width=13, anchor="w").pack(side="left")
            w = widget_fn(f)
            w.pack(side="left", fill="x", expand=True)
            return w

        today = datetime.date.today().strftime("%Y-%m-%d")

        date_var = tk.StringVar(value=expense["Date"] if expense else today)
        date_e   = field("Date", lambda f: tk.Entry(
            f, textvariable=date_var, font=("Helvetica",11),
            relief="flat", bg="#F5F5F4", fg=TEXT_PRI,
            insertbackground=TEXT_PRI))

        cat_var = tk.StringVar(value=expense["Category"] if expense else "Food")
        field("Category", lambda f: ttk.Combobox(
            f, textvariable=cat_var, values=CATEGORIES,
            state="readonly", font=("Helvetica",11)))

        desc_var = tk.StringVar(value=expense["Description"] if expense else "")
        desc_e   = field("Description", lambda f: tk.Entry(
            f, textvariable=desc_var, font=("Helvetica",11),
            relief="flat", bg="#F5F5F4", fg=TEXT_PRI,
            insertbackground=TEXT_PRI))

        amt_var = tk.StringVar(value=expense["Amount"] if expense else "")
        field("Amount (₹)", lambda f: tk.Entry(
            f, textvariable=amt_var, font=("Helvetica",11),
            relief="flat", bg="#F5F5F4", fg=TEXT_PRI,
            insertbackground=TEXT_PRI))

        # Buttons
        br = tk.Frame(dlg, bg=BG)
        br.pack(fill="x", padx=20, pady=16)

        def save_exp():
            date = date_var.get().strip()
            cat  = cat_var.get()
            desc = desc_var.get().strip() or cat
            try:
                amt = float(amt_var.get())
                if amt <= 0: raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid", "Enter a valid amount!", parent=dlg)
                return
            if expense:
                for ex in self.expenses:
                    if str(ex["ID"]) == str(expense["ID"]):
                        ex.update({"Date": date, "Category": cat,
                                   "Description": desc, "Amount": f"{amt:.2f}"})
                        break
            else:
                self.expenses.append({
                    "ID": next_id(self.expenses),
                    "Date": date, "Category": cat,
                    "Description": desc, "Amount": f"{amt:.2f}"
                })
            save(self.expenses)
            dlg.destroy()
            self.render()

        tk.Button(br, text="Save",
                  font=("Helvetica",11,"bold"),
                  bg=ACCENT, fg="white", relief="flat",
                  padx=20, pady=7, cursor="hand2",
                  activebackground=ACCENT_DK,
                  command=save_exp).pack(side="left", padx=(0,8))
        tk.Button(br, text="Cancel",
                  font=("Helvetica",11), relief="flat",
                  bg="#E8E7E2", fg=TEXT_PRI,
                  padx=16, pady=7, cursor="hand2",
                  command=dlg.destroy).pack(side="left")

        (date_e if not expense else desc_e).focus()
        dlg.bind("<Return>", lambda e: save_exp())

# ── Run ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    init_file()
    root = tk.Tk()
    root.tk_setPalette(background=BG)
    ExpenseApp(root)
    root.mainloop()
