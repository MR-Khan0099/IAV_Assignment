def perform_analysis(df):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import io
    import base64
    
    # Create a histogram of battery voltage
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Eng_uBatt', bins=20, kde=True)
    plt.xlabel('Battery Voltage (mV)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Battery Voltage')
    
    # Save the plot to a BytesIO object as a PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encode the image in base64
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_base64