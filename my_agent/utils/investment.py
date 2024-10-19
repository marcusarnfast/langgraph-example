def evaluate_investment(investment_risk: float, user_savings: float, user_income: float) -> str:
    """
    Evaluates whether an investment is a good idea based on the risk level,
    user's savings, and income.

    Parameters:
        investment_risk (float): The risk level of the investment (0.0 to 1.0).
        user_savings (float): The user's current savings amount.
        user_income (float): The user's income amount.

    Returns:
        str: A recommendation on whether the investment is a good idea.
    """
    # Simple evaluation logic
    if investment_risk > 0.7 and user_savings < 1000:
        return "Not a good idea"
    elif investment_risk <= 0.7 and user_income > 5000:
        return "Good idea"
    else:
        return "Consider your options"
