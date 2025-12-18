import streamlit as st

def calculate_roi(expected_yield, input_costs, market_price):
    """
    Calculate Return on Investment for crop production
    
    Args:
        expected_yield (float): Expected yield in tons per hectare
        input_costs (float): Total input costs in local currency per hectare
        market_price (float): Market price per ton in local currency
    
    Returns:
        dict: ROI analysis results
    """
    expected_revenue = expected_yield * market_price
    net_profit = expected_revenue - input_costs
    
    if input_costs > 0:
        roi_percentage = (net_profit / input_costs) * 100
    else:
        roi_percentage = 0
    
    if market_price > 0:
        break_even_yield = input_costs / market_price
    else:
        break_even_yield = 0
    
    return {
        'expected_revenue': expected_revenue,
        'net_profit': net_profit,
        'roi_percentage': roi_percentage,
        'break_even_yield': break_even_yield
    }

def optimize_fertilizer(current_fertilizer, fertilizer_price, crop_type, max_budget):
    """
    Optimize fertilizer usage for maximum ROI
    
    Args:
        current_fertilizer (float): Current fertilizer usage in kg/ha
        fertilizer_price (float): Price per kg of fertilizer
        crop_type (str): Type of crop
        max_budget (float): Maximum budget for fertilizer
    
    Returns:
        dict: Optimization results
    """
    # Crop-specific fertilizer response curves
    response_curves = {
        'Wheat': {'optimal': 120, 'max_response': 150},
        'Rice': {'optimal': 100, 'max_response': 130},
        'Corn': {'optimal': 140, 'max_response': 180},
        'Soybean': {'optimal': 80, 'max_response': 100}
    }
    
    crop_params = response_curves.get(crop_type, {'optimal': 100, 'max_response': 130})
    optimal_fertilizer = crop_params['optimal']
    
    # Calculate recommended fertilizer within budget
    recommended_fertilizer = min(optimal_fertilizer, max_budget / fertilizer_price)
    
    # Calculate expected improvement
    if current_fertilizer < recommended_fertilizer:
        improvement_ratio = (recommended_fertilizer - current_fertilizer) / current_fertilizer
        yield_improvement = min(improvement_ratio * 25, 50)  # Max 50% improvement
    else:
        yield_improvement = 0
    
    additional_cost = (recommended_fertilizer - current_fertilizer) * fertilizer_price
    
    return {
        'recommended_fertilizer': round(recommended_fertilizer, 1),
        'yield_improvement': yield_improvement,
        'additional_cost': additional_cost,
        'cost_effective': additional_cost <= max_budget
    }

def calculate_water_efficiency(water_used, yield_obtained, crop_type):
    """
    Calculate water use efficiency
    
    Args:
        water_used (float): Water used in cubic meters
        yield_obtained (float): Yield obtained in tons
        crop_type (str): Type of crop
    
    Returns:
        dict: Water efficiency metrics
    """
    if water_used > 0:
        water_efficiency = yield_obtained / water_used
    else:
        water_efficiency = 0
    
    # Benchmark values (tons per cubic meter)
    benchmarks = {
        'Wheat': 0.0015,
        'Rice': 0.0012,
        'Corn': 0.0018,
        'Soybean': 0.0010
    }
    
    benchmark = benchmarks.get(crop_type, 0.0013)
    efficiency_ratio = water_efficiency / benchmark if benchmark > 0 else 0
    
    return {
        'water_efficiency': water_efficiency,
        'benchmark': benchmark,
        'efficiency_ratio': efficiency_ratio,
        'efficiency_percentage': min(efficiency_ratio * 100, 200)  # Cap at 200%
    }