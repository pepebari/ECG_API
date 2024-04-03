from . import models, schemas


def calculate_insights(ecg: schemas.ECG):
    insights = {"zero_crossings": {}}
    for lead in ecg.leads:
        zero_crossings = 0
        signal = lead.signal
        for i in range(1, len(signal)):
            if signal[i-1] * signal[i] < 0:
                zero_crossings += 1
        insights["zero_crossings"][lead.name] = zero_crossings

    return schemas.ECGInsight(zero_crossings=insights["zero_crossings"])
