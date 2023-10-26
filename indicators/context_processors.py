from indicators.models import IndicatorData

def has_pending_indicator(request):
    # Your logic here to check for pending indicators
    has_pending = IndicatorData.objects.filter(status="pending").exists()
    return {'has_pending': has_pending}