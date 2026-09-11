import discord
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation


def _parse_infleta_range(raw_input: str) -> tuple[Decimal, Decimal]:
    cleaned = raw_input.strip()

    # Soporta "2 3", "2,3" (como separador) y decimales con coma.
    if " " in cleaned:
        parts = [p.strip() for p in cleaned.split() if p.strip()]
    else:
        parts = [p.strip() for p in cleaned.split(",") if p.strip()]

    if len(parts) != 2:
        raise ValueError("Formato invalido")

    try:
        first = Decimal(parts[0].replace(",", "."))
        second = Decimal(parts[1].replace(",", "."))
    except InvalidOperation:
        raise ValueError("Formato invalido")

    if first >= second:
        raise ValueError("Rango invalido")

    return first, second


def _format_decimal_spanish(value: Decimal) -> str:
    normalized = value.quantize(Decimal("0.1"))
    as_str = f"{normalized}"
    if as_str.endswith(".0"):
        as_str = as_str[:-2]
    return as_str.replace(".", ",")


def _build_infleta_options(start: Decimal, end: Decimal) -> list[str]:
    step = (end - start) / Decimal("10")
    if step <= 0:
        raise ValueError("Rango invalido")

    options = []
    for index in range(10):
        value = start + (step * Decimal(index))
        options.append(_format_decimal_spanish(value))

    return options


async def infletafun(interaction: discord.Interaction, rango: str) -> discord.Poll:
    if not hasattr(discord, "Poll"):
        raise RuntimeError("discord.py sin soporte de Poll")

    start, end = _parse_infleta_range(rango)
    options = _build_infleta_options(start, end)

    poll = discord.Poll(question="Valor de la infleta", duration=timedelta(hours=8))
    for option in options:
        poll.add_answer(text=option)

    # Log
    fecha_actual = datetime.now()
    print(fecha_actual)
    print(f"Se ha ejecutado el comando /infleta por {interaction.user}")

    return poll
