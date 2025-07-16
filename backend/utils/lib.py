from datetime import datetime, timezone

def format_timestamp(dt):
    if isinstance(dt, int):
        dt = datetime.fromtimestamp(dt, tz=timezone.utc)
    elif hasattr(dt, "to_native"):
        dt = dt.to_native()
        
    return dt.strftime("%b %d, %Y %I:%M %p") if dt else None


def cypher_duration_since_rating(rel_alias: str = "r", timestamp_field: str = "timestamp") -> str:
    """
    Returns Cypher expression to calculate duration (years, months, days) since rating timestamp.
    """
    return (
        f"duration.between(datetime({{epochMillis: {rel_alias}.{timestamp_field} * 1000}}), datetime()) AS durationSinceRated"
    )


def format_duration(duration) -> str:
    if duration is None:
        return "unknown time"

    parts = []

    # Convert total months into years and remaining months
    total_months = getattr(duration, "months", 0)
    years_from_months = total_months // 12
    remaining_months = total_months % 12

    # Add years (from .years field plus years converted from months)
    total_years = getattr(duration, "years", 0) + years_from_months
    if total_years > 0:
        parts.append(f"{total_years} year{'s' if total_years != 1 else ''}")

    # Add remaining months
    if remaining_months > 0:
        parts.append(f"{remaining_months} month{'s' if remaining_months != 1 else ''}")

    # Add days
    days = getattr(duration, "days", 0)
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")

    if not parts:
        return "0 days"

    return " ".join(parts)