from enum import Enum


# class syntax
class ResearchExpenseType(Enum):
    incurred = {
        "tag": "ResearchAndDevelopmentExpense",
        "readable_name": "rd_expense"
    }
    DEFERRED = {
        "tag": "DeferredResearchAndDevelopmentExpense",
        "readable_name": "deferred_rd_expense"
    }
    CAPITALIZED = {
        "tag": "CapitalizedResearchAndDevelopmentCosts",
        "readable_name": "capitalized_rd_costs"
    }
