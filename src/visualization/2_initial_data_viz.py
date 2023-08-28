#%%
# Plot Features Over Time
n_columns = len(df_raw.axes[1]) - 1

for i in range(n_columns):
    series = df_raw.iloc[:,i+1]
    file_name = os.path.join(FIGURES_PATH, f"raw_eda/line/{i}_{series.name}.html")

    fig = px.line(df_raw, x=df_raw.index, y=series)
    fig.update_layout(yaxis_title=series.name, xaxis_title="Time")
    fig.show()
    plt(fig, filename=file_name)

# The % Silica Concentrate don't show any "global" seazonality, 
# also it doesnt apear to show any trend