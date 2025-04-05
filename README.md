# National Parks Visualization Tool | 美国国家公园可视化工具

This project visualizes U.S. national park data including locations, campgrounds, webcams, and visitor centers on an interactive map using Folium.  
本项目基于 Folium 库实现美国国家公园的位置、营地、摄像头、游客中心等数据的交互式地图展示。

---

## API Key Required (Optional) | 需要 API 密钥（可选）

To run the full pipeline and generate up-to-date data, you must apply for an API key from the [National Park Service Developer Portal](https://www.nps.gov/subjects/developer/api-documentation.htm).  
如需生成最新数据，您需要前往 [NPS 官方开发者平台](https://www.nps.gov/subjects/developer/api-documentation.htm) 申请 API 密钥。

The source code uses `"111"` as a placeholder. Please replace it with your own key in the following files:  
源码中将 `"111"` 作为占位符，请在以下文件中替换为您自己的 API 密钥：

- `match_parks_nps.py`
- `campdata.py`
- `Visitor_Centers.py`
- `webcams.py`

If you don’t have a key, you can still run `map_view.py`, which uses the datasets generated on **April 5, 2025**.  
如果没有密钥，也可以直接运行 `map_view.py` 使用 2025 年 4 月 5 日生成的静态数据。

---

## Project Structure | 项目结构说明

| File 文件 | Purpose 说明 |
|-----------|---------------|
| `main.py` | Run this to trigger the entire data collection and map generation pipeline. 运行主程序，完成数据收集与地图生成。 |
| `map_view.py` | Generates the interactive map using CSV files. 基于 CSV 数据生成交互地图。 |
| `match_parks_nps.py` | Matches official park names with NPS database entries via API. 将 63 个官方公园名称与 NPS 数据库进行匹配。 |
| `campdata.py` | Fetches campground info per park. 获取每个国家公园的营地信息。 |
| `Visitor_Centers.py` | Retrieves visitor center details (name, hours, etc). 获取游客中心的详情（名称、开放时间等）。 |
| `webcams.py` | Collects webcam live stream info for each park. 获取每个公园的摄像头直播信息。 |
| `get_park_names.py` | Contains the list of 63 official U.S. national parks. 包含官方定义的 63 个国家公园名称列表。 |

---

## Output Datasets | 输出数据文件

以下数据文件为中间产物，供地图渲染使用：

- `matched_national_parks.csv`: matched park names and coordinates 公园名称与坐标匹配结果
- `campgrounds_data.csv`: campground data 营地数据
- `visitor_centers.csv`: visitor center data 游客中心数据
- `nps_webcams.csv`: webcam information 摄像头信息

---

## Technical Highlights | 技术实现亮点

- **Libraries 使用的库**:  
  `pandas`, `requests`, `folium`, `re` (正则表达式), `json`, `csv`

- **Map Rendering 地图渲染**:  
  Using `folium` to render a base map with toggleable layers for parks, campgrounds, visitor centers, and webcams.  
  使用 Folium 实现地图基础图层，并支持不同功能图层切换。

- **Data Retrieval 数据获取**:  
  Uses official NPS API to retrieve data programmatically.  
  利用 NPS 官方 API 实时获取国家公园数据。

- **Web Scraping 爬虫应用**:  
  The `get_park_names.py` script simulates the process of extracting park names from Wikipedia using manual preprocessing.  
  `get_park_names.py` 模拟网页抓取逻辑处理维基百科公园名称数据（实际可用于真实爬虫逻辑扩展）。

- **Regular Expression 正则表达式处理**:  
  Name matching relies on regular expressions to standardize and normalize park names.  
  使用正则表达式清洗与标准化公园名称用于匹配。

- **Data Cleaning 数据清洗与标准化**:  
  Cleaning missing values, converting number formats, merging heterogeneous fields.  
  包括缺失值处理、字符串格式转换、字段合并等预处理操作。

- **Error Handling 错误处理机制**:  
  All data fetch functions include exception catching for robustness.  
  所有数据处理函数均包含异常捕捉机制，提升稳定性。

- **Modular Design 模块化设计**:  
  Each feature is encapsulated in an independent script and can be used or replaced independently.  
  每个功能均模块化设计，便于替换与调试，支持未来封装成 OOP 或类库结构。

---

Feel free to fork this project and adapt it to your own needs.  
欢迎 fork 本项目进行二次开发或个性化定制。
