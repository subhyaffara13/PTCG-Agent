
def _get_projected_spend_over_limit(
    current_spend: float, soft_budget_limit: Optional[float]
) -> Optional[tuple]:
    if soft_budget_limit is None:
        return None

    today = date.today()
    end_month = _get_month_end_date(today)
    remaining_days = (end_month - today).days

    # assuming the current spend till today (not including today)
    if today.day == 1:
        daily_spend = current_spend
    else:
        daily_spend = current_spend / (today.day - 1)
    projected_spend = current_spend + (daily_spend * remaining_days)

    if projected_spend > soft_budget_limit:
        if daily_spend <= 0:
            limit_exceed_date = today
        else:
            remaining_budget = soft_budget_limit - current_spend
            if remaining_budget <= 0:
                limit_exceed_date = today
            else:
                approx_days = remaining_budget / daily_spend
                limit_exceed_date = today + timedelta(days=approx_days)

        # return the projected spend and the date it will exceeded
        return projected_spend, limit_exceed_date

    return None

