import os
import tkinter as tk
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from threading import Thread
from tkinter import messagebox, ttk

import requests


# Add your Alpha Vantage API key as an environment variable.
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "E0FSB4U1KDNCHITX")
API_URL = "https://www.alphavantage.co/query"


CURRENCIES = {
    "AED": "UAE Dirham",
    "ARS": "Argentine Peso",
    "AUD": "Australian Dollar",
    "BGN": "Bulgarian Lev",
    "BHD": "Bahraini Dinar",
    "BRL": "Brazilian Real",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CLP": "Chilean Peso",
    "CNY": "Chinese Yuan",
    "COP": "Colombian Peso",
    "CZK": "Czech Koruna",
    "DKK": "Danish Krone",
    "EGP": "Egyptian Pound",
    "EUR": "Euro",
    "GBP": "British Pound",
    "GHS": "Ghanaian Cedi",
    "HKD": "Hong Kong Dollar",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli New Shekel",
    "INR": "Indian Rupee",
    "ISK": "Icelandic Krona",
    "JPY": "Japanese Yen",
    "KES": "Kenyan Shilling",
    "KRW": "South Korean Won",
    "KWD": "Kuwaiti Dinar",
    "MAD": "Moroccan Dirham",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "NGN": "Nigerian Naira",
    "NOK": "Norwegian Krone",
    "NZD": "New Zealand Dollar",
    "PEN": "Peruvian Sol",
    "PHP": "Philippine Peso",
    "PKR": "Pakistani Rupee",
    "PLN": "Polish Zloty",
    "QAR": "Qatari Riyal",
    "RON": "Romanian Leu",
    "RSD": "Serbian Dinar",
    "SAR": "Saudi Riyal",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "THB": "Thai Baht",
    "TRY": "Turkish Lira",
    "TWD": "Taiwan Dollar",
    "UAH": "Ukrainian Hryvnia",
    "USD": "US Dollar",
    "VND": "Vietnamese Dong",
    "ZAR": "South African Rand",
}


THEMES = {
    "light": {
        "window": "#eef2f7",
        "card": "#ffffff",
        "input": "#f8fafc",
        "text": "#172033",
        "secondary_text": "#64748b",
        "border": "#d8dee9",
        "primary": "#2563eb",
        "primary_hover": "#1d4ed8",
        "secondary_button": "#e2e8f0",
        "secondary_button_hover": "#cbd5e1",
        "result": "#0f766e",
        "selection": "#bfdbfe",
    },
    "dark": {
        "window": "#101216",
        "card": "#1b1f27",
        "input": "#252a34",
        "text": "#f8fafc",
        "secondary_text": "#a6adbb",
        "border": "#353b47",
        "primary": "#3b82f6",
        "primary_hover": "#60a5fa",
        "secondary_button": "#303641",
        "secondary_button_hover": "#414957",
        "result": "#5eead4",
        "selection": "#1d4ed8",
    },
}


def currency_option(code):
    return f"{code} — {CURRENCIES[code]}"


def extract_currency_code(option):
    return option.split(" — ", 1)[0]


class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("660x570")
        self.root.minsize(570, 520)

        self.current_theme = "light"

        self.amount_var = tk.StringVar()

        self.from_currency_var = tk.StringVar(
            value=currency_option("EUR")
        )

        self.to_currency_var = tk.StringVar(
            value=currency_option("USD")
        )

        self.result_var = tk.StringVar(value="—")
        self.rate_var = tk.StringVar(value="Exchange rate: —")
        self.status_var = tk.StringVar(value="Ready")

        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.create_widgets()
        self.apply_theme()

        self.root.bind(
            "<Return>",
            lambda event: self.start_conversion()
        )

        self.amount_entry.focus_set()

    def create_widgets(self):
        self.container = ttk.Frame(
            self.root,
            padding=24,
            style="Page.TFrame"
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        header = ttk.Frame(
            self.container,
            style="Page.TFrame"
        )

        header.pack(
            fill="x",
            pady=(0, 18)
        )

        header.columnconfigure(0, weight=1)

        title_container = ttk.Frame(
            header,
            style="Page.TFrame"
        )

        title_container.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ttk.Label(
            title_container,
            text="Currency Converter",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            title_container,
            text="Convert currencies using live exchange rates",
            style="Subtitle.TLabel"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        self.theme_button = ttk.Button(
            header,
            text="Dark Mode",
            command=self.toggle_theme,
            style="Theme.TButton"
        )

        self.theme_button.grid(
            row=0,
            column=1,
            sticky="ne"
        )

        self.card = ttk.Frame(
            self.container,
            padding=24,
            style="Card.TFrame"
        )

        self.card.pack(
            fill="both",
            expand=True
        )

        self.card.columnconfigure(0, weight=1)
        self.card.columnconfigure(1, weight=0)
        self.card.columnconfigure(2, weight=1)

        ttk.Label(
            self.card,
            text="From Currency",
            style="CardLabel.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ttk.Label(
            self.card,
            text="To Currency",
            style="CardLabel.TLabel"
        ).grid(
            row=0,
            column=2,
            sticky="w"
        )

        currency_options = [
            currency_option(code)
            for code in sorted(CURRENCIES)
        ]

        self.from_combo = ttk.Combobox(
            self.card,
            textvariable=self.from_currency_var,
            values=currency_options,
            state="readonly",
            style="Currency.TCombobox",
            font=("Segoe UI", 10)
        )

        self.from_combo.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(7, 20)
        )

        self.swap_button = ttk.Button(
            self.card,
            text="⇄",
            command=self.swap_currencies,
            style="Secondary.TButton",
            width=4
        )

        self.swap_button.grid(
            row=1,
            column=1,
            padx=12,
            pady=(7, 20)
        )

        self.to_combo = ttk.Combobox(
            self.card,
            textvariable=self.to_currency_var,
            values=currency_options,
            state="readonly",
            style="Currency.TCombobox",
            font=("Segoe UI", 10)
        )

        self.to_combo.grid(
            row=1,
            column=2,
            sticky="ew",
            pady=(7, 20)
        )

        ttk.Label(
            self.card,
            text="Amount",
            style="CardLabel.TLabel"
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="w"
        )

        self.amount_entry = ttk.Entry(
            self.card,
            textvariable=self.amount_var,
            style="Amount.TEntry",
            font=("Segoe UI", 14)
        )

        self.amount_entry.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(7, 20),
            ipady=8
        )

        self.convert_button = ttk.Button(
            self.card,
            text="Convert",
            command=self.start_conversion,
            style="Primary.TButton"
        )

        self.convert_button.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=(0, 8)
        )

        self.clear_button = ttk.Button(
            self.card,
            text="Clear",
            command=self.clear_all,
            style="Secondary.TButton"
        )

        self.clear_button.grid(
            row=4,
            column=2,
            sticky="ew"
        )

        ttk.Separator(
            self.card,
            style="Custom.TSeparator"
        ).grid(
            row=5,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=24
        )

        ttk.Label(
            self.card,
            text="Converted Amount",
            style="CardLabel.TLabel"
        ).grid(
            row=6,
            column=0,
            columnspan=3,
            sticky="w"
        )

        ttk.Label(
            self.card,
            textvariable=self.result_var,
            style="Result.TLabel"
        ).grid(
            row=7,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(8, 5)
        )

        ttk.Label(
            self.card,
            textvariable=self.rate_var,
            style="Rate.TLabel"
        ).grid(
            row=8,
            column=0,
            columnspan=3,
            sticky="w"
        )

        ttk.Label(
            self.container,
            textvariable=self.status_var,
            style="Status.TLabel"
        ).pack(
            anchor="w",
            pady=(11, 0)
        )

    def apply_theme(self):
        theme = THEMES[self.current_theme]

        self.root.configure(
            bg=theme["window"]
        )

        self.style.configure(
            "Page.TFrame",
            background=theme["window"]
        )

        self.style.configure(
            "Card.TFrame",
            background=theme["card"]
        )

        self.style.configure(
            "Title.TLabel",
            background=theme["window"],
            foreground=theme["text"],
            font=("Segoe UI", 23, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            background=theme["window"],
            foreground=theme["secondary_text"],
            font=("Segoe UI", 10)
        )

        self.style.configure(
            "CardLabel.TLabel",
            background=theme["card"],
            foreground=theme["text"],
            font=("Segoe UI", 10, "bold")
        )

        self.style.configure(
            "Result.TLabel",
            background=theme["card"],
            foreground=theme["result"],
            font=("Segoe UI", 25, "bold")
        )

        self.style.configure(
            "Rate.TLabel",
            background=theme["card"],
            foreground=theme["secondary_text"],
            font=("Segoe UI", 10)
        )

        self.style.configure(
            "Status.TLabel",
            background=theme["window"],
            foreground=theme["secondary_text"],
            font=("Segoe UI", 9)
        )

        self.style.configure(
            "Primary.TButton",
            background=theme["primary"],
            foreground="#ffffff",
            borderwidth=0,
            padding=(16, 11),
            font=("Segoe UI", 10, "bold")
        )

        self.style.map(
            "Primary.TButton",
            background=[
                ("active", theme["primary_hover"]),
                ("pressed", theme["primary_hover"]),
                ("disabled", theme["border"])
            ],
            foreground=[
                ("disabled", theme["secondary_text"])
            ]
        )

        self.style.configure(
            "Secondary.TButton",
            background=theme["secondary_button"],
            foreground=theme["text"],
            borderwidth=0,
            padding=(12, 11),
            font=("Segoe UI", 10)
        )

        self.style.map(
            "Secondary.TButton",
            background=[
                ("active", theme["secondary_button_hover"]),
                ("pressed", theme["secondary_button_hover"])
            ],
            foreground=[
                ("active", theme["text"])
            ]
        )

        self.style.configure(
            "Theme.TButton",
            background=theme["secondary_button"],
            foreground=theme["text"],
            borderwidth=0,
            padding=(13, 9),
            font=("Segoe UI", 9, "bold")
        )

        self.style.map(
            "Theme.TButton",
            background=[
                ("active", theme["secondary_button_hover"]),
                ("pressed", theme["secondary_button_hover"])
            ],
            foreground=[
                ("active", theme["text"])
            ]
        )

        self.style.configure(
            "Amount.TEntry",
            fieldbackground=theme["input"],
            foreground=theme["text"],
            bordercolor=theme["border"],
            lightcolor=theme["border"],
            darkcolor=theme["border"],
            padding=8
        )

        self.style.map(
            "Amount.TEntry",
            fieldbackground=[
                ("focus", theme["input"])
            ],
            foreground=[
                ("focus", theme["text"])
            ],
            bordercolor=[
                ("focus", theme["primary"])
            ]
        )

        self.style.configure(
            "Currency.TCombobox",
            fieldbackground=theme["input"],
            background=theme["input"],
            foreground=theme["text"],
            arrowcolor=theme["text"],
            bordercolor=theme["border"],
            lightcolor=theme["border"],
            darkcolor=theme["border"],
            padding=7
        )

        self.style.map(
            "Currency.TCombobox",
            fieldbackground=[
                ("readonly", theme["input"])
            ],
            background=[
                ("readonly", theme["input"]),
                ("active", theme["input"])
            ],
            foreground=[
                ("readonly", theme["text"])
            ],
            arrowcolor=[
                ("readonly", theme["text"]),
                ("active", theme["primary"])
            ],
            bordercolor=[
                ("focus", theme["primary"])
            ]
        )

        self.style.configure(
            "Custom.TSeparator",
            background=theme["border"]
        )

        # Colors for the Combobox dropdown list.
        self.root.option_add(
            "*TCombobox*Listbox.background",
            theme["input"]
        )

        self.root.option_add(
            "*TCombobox*Listbox.foreground",
            theme["text"]
        )

        self.root.option_add(
            "*TCombobox*Listbox.selectBackground",
            theme["selection"]
        )

        self.root.option_add(
            "*TCombobox*Listbox.selectForeground",
            "#ffffff"
        )

        if self.current_theme == "light":
            self.theme_button.configure(text="Dark Mode")
        else:
            self.theme_button.configure(text="Light Mode")

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.status_var.set("Dark theme enabled.")
        else:
            self.current_theme = "light"
            self.status_var.set("Light theme enabled.")

        self.apply_theme()

    def start_conversion(self):
        raw_amount = self.amount_var.get().strip()
        raw_amount = raw_amount.replace(",", ".")

        try:
            amount = Decimal(raw_amount)

            if not amount.is_finite() or amount < 0:
                raise InvalidOperation

        except InvalidOperation:
            messagebox.showerror(
                "Invalid Amount",
                "Enter a valid positive number."
            )
            return

        from_currency = extract_currency_code(
            self.from_currency_var.get()
        )

        to_currency = extract_currency_code(
            self.to_currency_var.get()
        )

        if from_currency == to_currency:
            self.show_result(
                amount,
                Decimal("1"),
                from_currency,
                to_currency
            )
            return

        if API_KEY == "YOUR_API_KEY_HERE":
            messagebox.showerror(
                "Missing API Key",
                "Set the ALPHA_VANTAGE_API_KEY environment variable "
                "or enter your API key in the API_KEY variable."
            )
            return

        self.convert_button.configure(
            state="disabled"
        )

        self.status_var.set(
            "Fetching the latest exchange rate..."
        )

        worker = Thread(
            target=self.fetch_exchange_rate,
            args=(
                amount,
                from_currency,
                to_currency
            ),
            daemon=True
        )

        worker.start()

    def fetch_exchange_rate(
        self,
        amount,
        from_currency,
        to_currency
    ):
        try:
            response = requests.get(
                API_URL,
                params={
                    "function": "CURRENCY_EXCHANGE_RATE",
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "apikey": API_KEY
                },
                timeout=15
            )

            response.raise_for_status()
            data = response.json()

            rate_data = data.get(
                "Realtime Currency Exchange Rate"
            )

            if not rate_data:
                api_message = (
                    data.get("Note")
                    or data.get("Information")
                    or data.get("Error Message")
                    or "The API did not return a valid exchange rate."
                )

                raise ValueError(api_message)

            rate = Decimal(
                rate_data["5. Exchange Rate"]
            )

            self.root.after(
                0,
                lambda: self.show_result(
                    amount,
                    rate,
                    from_currency,
                    to_currency
                )
            )

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            InvalidOperation
        ) as error:

            error_message = str(error)

            self.root.after(
                0,
                lambda: self.show_error(error_message)
            )

    def show_result(
        self,
        amount,
        rate,
        from_currency,
        to_currency
    ):
        converted = (amount * rate).quantize(
            Decimal("0.001"),
            rounding=ROUND_HALF_UP
        )

        self.result_var.set(
            f"{converted:,.3f} {to_currency}"
        )

        self.rate_var.set(
            f"1 {from_currency} = "
            f"{rate:.6f} {to_currency}"
        )

        self.status_var.set(
            "Conversion completed successfully."
        )

        self.convert_button.configure(
            state="normal"
        )

    def show_error(self, error):
        self.status_var.set(
            "Conversion failed."
        )

        self.convert_button.configure(
            state="normal"
        )

        messagebox.showerror(
            "Conversion Error",
            f"Unable to complete the conversion.\n\n{error}"
        )

    def swap_currencies(self):
        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()

        self.from_currency_var.set(to_currency)
        self.to_currency_var.set(from_currency)

        self.result_var.set("—")
        self.rate_var.set("Exchange rate: —")
        self.status_var.set("Currencies swapped.")

    def clear_all(self):
        self.amount_var.set("")
        self.result_var.set("—")
        self.rate_var.set("Exchange rate: —")
        self.status_var.set("Ready")
        self.amount_entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()