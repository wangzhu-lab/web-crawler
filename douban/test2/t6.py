from pyecharts.charts import MapGlobe

POPULATION_name_has_modified = POPULATION_df[['EchartsNameEN','Population']].values.tolist()

#data = [x for _, x in POPULATION[1:]]
data = [x for _, x in POPULATION_name_has_modified]
low, high = min(data), max(data)

mg = (
    MapGlobe(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_schema()
    .add(
        maptype="world",
        series_name="World Population",
        data_pair=POPULATION_name_has_modified,
        is_map_symbol_show=False,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            min_=low,
            max_=high,
            range_text=["max", "min"],
            is_calculable=True,
            range_color=["lightskyblue", "yellow", "red"],
        )
    )
)
mg.render_notebook()