# LLM Wiki Processor

一个用于处理小红书视频并整合到知识库的系统，支持视频下载、音频提取、语音转文字和内容摄入等功能。

## 项目结构

```
llm-wiki-processor/
├── backend/          # 后端服务
│   ├── src/          # 源代码
│   │   ├── app.py              # 主应用
│   │   └── modules/            # 功能模块
│   │       └── video_downloader/  # 视频下载模块
│   ├── requirements.txt        # 依赖配置
│   └── start.bat               # 启动脚本
├── frontend/         # 前端应用
│   ├── src/          # 源代码
│   │   ├── App.jsx             # 主应用组件
│   │   ├── main.jsx            # 入口文件
│   │   ├── index.css           # 样式文件
│   │   └── App.css             # 应用样式
│   ├── package.json            # 依赖配置
│   ├── vite.config.js          # Vite配置
│   ├── tailwind.config.js      # Tailwind配置
│   ├── postcss.config.js       # PostCSS配置
│   └── index.html              # HTML模板
└── README.md         # 项目文档
```

## 技术栈

### 后端
- Python 3.8+
- 内置 HTTP 服务器
- 视频下载模块

### 前端
- React 18.2.0
- Tailwind CSS 3.4.0
- Vite 5.0.8

## 核心功能

1. **视频链接解析**：支持小红书官方链接和 xhslink 格式
2. **视频信息获取**：获取视频的标题、作者、描述等元数据
3. **视频下载**：从小红书服务器下载视频文件
4. **错误处理**：处理各种异常情况，如链接无效、下载失败等
5. **前端界面**：提供直观的用户界面，支持视频链接输入、处理状态显示和结果展示

## 安装与使用

### 后端服务

1. **安装依赖**：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **启动服务**：
   ```bash
   cd src
   python app.py
   ```

3. **服务地址**：
   - 服务运行在 `http://localhost:3001`
   - 健康检查接口：`http://localhost:3001/api/health`
   - 视频处理接口：`http://localhost:3001/api/process`

### 前端应用

1. **安装依赖**：
   ```bash
   cd frontend
   npm install
   ```

2. **启动开发服务器**：
   ```bash
   npm run dev
   ```

3. **访问应用**：
   - 应用运行在 `http://localhost:3000`

## API 接口

### 1. 健康检查

**请求**：
```http
GET /api/health
```

**响应**：
```json
{
  "status": "ok",
  "message": "LLM Wiki Processor is running"
}
```

### 2. 视频处理

**请求**：
```http
POST /api/process
Content-Type: application/json

{
  "video_url": "https://www.xiaohongshu.com/explore/69b824b0000000001d01c798"
}
```

**响应**：
```json
{
  "status": "success",
  "video_info": {
    "video_id": "69b824b0000000001d01c798",
    "title": "小红书视频 69b824b0000000001d01c798",
    "author": "模拟用户",
    "description": "这是一个模拟的小红书视频描述",
    "duration": 60,
    "cover_url": "https://example.com/covers/69b824b0000000001d01c798.jpg",
    "video_url": "https://example.com/videos/69b824b0000000001d01c798.mp4",
    "likes": 1000,
    "comments": 100,
    "shares": 50
  },
  "download_path": "Z:\RnVFamily\RyanKKLam\Workspace\llm-wiki-dimple\llm-wiki-processor\backend\temp\69b824b0000000001d01c798.mp4",
  "message": "Video processed successfully"
}
```

## 使用指南

1. **打开前端应用**：访问 `http://localhost:3000`
2. **输入视频链接**：在输入框中粘贴小红书视频链接
3. **点击开始处理**：系统会自动解析链接、获取视频信息并下载视频
4. **查看结果**：处理完成后，系统会显示视频信息和下载路径

## 注意事项

1. **网络连接**：确保网络连接正常，以便能够访问小红书服务器
2. **链接格式**：支持小红书官方链接和 xhslink 格式
3. **下载限制**：小红书可能有访问限制，下载速度可能会受到影响
4. **存储空间**：确保有足够的存储空间来保存下载的视频文件

## 故障排除

### 常见问题

1. **后端服务启动失败**：
   - 检查 Python 是否已正确安装
   - 检查依赖是否已正确安装
   - 检查端口 3001 是否被占用

2. **前端应用无法连接到后端**：
   - 确保后端服务已启动
   - 检查前端配置中的后端地址是否正确

3. **视频下载失败**：
   - 检查网络连接
   - 检查视频链接是否有效
   - 尝试使用不同的视频链接

## 后续计划

1. **音频提取**：从下载的视频中提取音频
2. **语音转文字**：将提取的音频转换为文本
3. **内容摄入**：将转换后的文本内容整合到知识库
4. **批量处理**：支持批量处理多个视频
5. **用户认证**：添加用户认证功能

## 许可证

MIT License
