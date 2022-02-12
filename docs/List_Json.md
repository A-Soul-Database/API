## List_Json -Api  
Main,Cover及Indexer 的筛选,搜索  
#### 用法  
Host: `https://apihk.asdb.live/Main/V1`  
- 列出所有`Main.json`  
`Get /Main_Data`  
可选参数  
```
reverse    int(0/1)     正/逆序
bv         str          特定Bv号
```
响应体  
```json
    {   
        "code":0,
        "msg":"ok",
        "data":{"..."}
    }
```

- 列出所有封面链接  
`Get /Cover_Data`  
可选参数  
```
bv          str         特定Bv号
```
响应体  
```json
    {   
        "code":0,
        "msg":"ok",
        "data":{"Bv1":"https://..."}
    }
```  

- 列出所有`Indexer`
因为`Main.json`是一个列表,包含着`Dicts`,无法直接通过Bv号定位.但是你可以通过Indexer使用Bv号定位  
`Get /Indexer_Data`
可选参数  
```
bv          str         特定Bv号
```
响应体  
```json
    {   
        "code":0,
        "msg":"ok",
        "data":["Bv1","Bv2"]
    }
        {   
        "code":0,
        "msg":"ok",
        "data":73 //以Bv参数请求时会返回位置
    }
```

- 获取字幕链接  
`Get /Srt_Data`
必要参数  
```
bv          str         特定Bv号
```
响应体  
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "name": [
      "BV1554y147v2-1.srt",
      "BV1554y147v2-2.srt"
    ],
    "url": [
      "/db/2021/01/srt/BV1554y147v2-1.srt",
      "/db/2021/01/srt/BV1554y147v2-2.srt"
    ],
    "sources": [
      "https://raw.githubusercontent.com/A-Soul-Database/A-Soul-Data/main",
      "https://cdn.jsdelivr.net/gh/A-Soul-Database/A-Soul-Data@latest/db" //对于某些地区无法访问githubcontents,可以通过jsdeliever访问
    ]
  }
}
```

- 筛选`Main.json`  
`Post /Main_Fliter`
请求体  
```json
    {
        "bv":"",  //Bv号,如果请求中带有Bv号则直接返回响应的Bv项
        "liveroom":"",  //直播间位置, "A" -> 向晚 ...
        "title":"",  //直播标题
        "staff":[],  //出场成员 ["A","B"...]
        "scene":[], //场景
        "skin":[],  //服饰
        "types":[], //类型 ["song","game"]
        "keywords":"",  //关键词
        "reverse":0   //排序方式
    }
```

#### 错误排查
- 无Bv号  
`{"code":-1,"msg":"No Bv"}`  
- 数据正在初始化/更新
`{"code":-1,"msg":"Data Initializing or Updating"}`
