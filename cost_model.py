
import json

def load_base_rates(path="data/base_rates.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def estimate_cost(params, base_rates):
    project_type = params["project_type"]
    area = params["area"]
    resin_price = params["resin_price"]

    rates = base_rates["project_profiles"][project_type]
    fiber_weight = sum(rates["layers"].values()) * rates["fiber_consumption"] * area
    resin_weight = fiber_weight * rates["resin_multiplier"]
    resin_cost = resin_weight * resin_price

    base_npr = base_rates["labor_rates"][project_type]
    labor_cost = base_npr * area * base_rates["labor_unit_rate"] * params["difficulty_factor"]

    equip_cost = base_rates["fixed_equipment_costs"].get(project_type, 0)

    material_cost = resin_cost
    total = material_cost + labor_cost + equip_cost

    overhead = base_rates["overhead_rate"]
    profit = base_rates["profit_rate"]
    total_with_markup = total * (1 + overhead + profit)

    return {
        "material_cost": material_cost,
        "labor_cost": labor_cost,
        "equip_cost": equip_cost,
        "total_before_markup": total,
        "total_price": total_with_markup,
        "price_per_m2": total_with_markup / area
    }
