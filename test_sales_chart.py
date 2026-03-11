"""
Test file for sales_chart_app.py
Demonstrates using assert statements to test pure functions
"""

from sales_chart_app import calculate_totals, read_csv


def test_calculate_totals_basic():
    """Test calculate_totals with basic data."""
    test_data = [
        {"month": "January", "snow": 10, "temperature": -10},
        {"month": "February", "snow": 20, "temperature": -5}
    ]
    
    result = calculate_totals(test_data)
    
    assert result["total_snow"] == 30, "Total snow should be 30"
    assert result["avg_temp"] == -7.5, "Average temp should be -7.5"
    
    print("✓ Basic totals test passed!")


def test_calculate_totals_empty():
    """Test calculate_totals with empty data."""
    result = calculate_totals([])
    
    assert result["total_snow"] == 0, "Empty list should return 0 total_snow"
    assert result["avg_temp"] == 0, "Empty list should return 0 avg_temp"
    
    print("✓ Empty data test passed!")


def test_calculate_totals_single_item():
    """Test calculate_totals with a single item."""
    test_data = [
        {"month": "January", "snow": 15, "temperature": 5}
    ]
    
    result = calculate_totals(test_data)
    
    assert result["total_snow"] == 15, "Single item total_snow should be 15"
    assert result["avg_temp"] == 5.0, "Single item avg_temp should be 5.0"
    
    print("✓ Single item test passed!")


def test_calculate_totals_large_numbers():
    """Test calculate_totals with large numbers."""
    test_data = [
        {"month": "January", "snow": 100, "temperature": -20},
        {"month": "February", "snow": 200, "temperature": -15}
    ]
    
    result = calculate_totals(test_data)
    
    assert result["total_snow"] == 300, "Large numbers should calculate correctly"
    assert result["avg_temp"] == -17.5, "Average temp should calculate correctly"
    
    print("✓ Large numbers test passed!")


def test_calculate_totals_loss_scenario():
    """Test calculate_totals with negative temperatures."""
    test_data = [
        {"month": "January", "snow": 25, "temperature": -30}
    ]
    
    result = calculate_totals(test_data)
    
    assert result["total_snow"] == 25
    assert result["avg_temp"] == -30.0
    
    print("✓ Negative temperature scenario test passed!")


def test_calculate_totals_zero_values():
    """Test calculate_totals with zero values."""
    test_data = [
        {"month": "January", "snow": 0, "temperature": 0}
    ]
    
    result = calculate_totals(test_data)
    
    assert result["total_snow"] == 0
    assert result["avg_temp"] == 0.0
    
    print("✓ Zero values test passed!")


def run_all_tests():
    """Run all test functions."""
    print("Running tests for calculate_totals()...\n")
    
    try:
        test_calculate_totals_basic()
        test_calculate_totals_empty()
        test_calculate_totals_single_item()
        test_calculate_totals_large_numbers()
        test_calculate_totals_loss_scenario()
        test_calculate_totals_zero_values()
        
        print("\n" + "="*50)
        print("All tests passed! ✓")
        print("="*50)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        raise
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
