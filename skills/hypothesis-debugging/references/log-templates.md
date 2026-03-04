# 日志代码模板

本文档包含各种编程语言的 Debug Mode 日志代码模板。

## 路径说明

**日志文件固定路径**：`~/.codeflicker/debug.log`

- **浏览器环境**：通过 HTTP POST 发送到日志服务器，服务器写入固定路径
- **Node.js/Python/其他后端**：可以直接写文件或通过 HTTP POST

## 通用规则

1. **必须使用 region 标记** - 便于识别和批量清理
2. **必须包含 hypothesisId** - 关联到具体假设
3. **必须包含 runId** - 区分不同运行
4. **必须包含 location** - 文件名:行号
5. **尽量紧凑** - 一行或几行完成，减少代码污染

## JavaScript / TypeScript

### 浏览器环境（HTTP POST）

```typescript
// #region debug-mode-log
fetch('http://127.0.0.1:7491',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({hypothesisId:'H1',runId:'run-1',location:'file.ts:42',message:'updateUser START',data:{userId,state},timestamp:Date.now()})}).catch(()=>{});
// #endregion debug-mode-log
```

### 多行格式（更易读）

```typescript
// #region debug-mode-log
fetch('http://127.0.0.1:7491', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    hypothesisId: 'H1',
    runId: 'run-1',
    location: 'file.ts:42',
    message: 'updateUser START',
    data: { userId, state },
    timestamp: Date.now()
  })
}).catch(() => {});
// #endregion debug-mode-log
```

### Node.js（直接写文件）

```typescript
// #region debug-mode-log
const os = require('os');
require('fs').appendFileSync(os.homedir() + '/.codeflicker/debug.log', JSON.stringify({hypothesisId:'H1',runId:'run-1',location:'file.ts:42',message:'desc',data:{},timestamp:Date.now()})+'\n');
// #endregion debug-mode-log
```

### Node.js（ES Module）

```typescript
// #region debug-mode-log
import { appendFileSync } from 'fs';
import { homedir } from 'os';
appendFileSync(homedir() + '/.codeflicker/debug.log', JSON.stringify({hypothesisId:'H1',runId:'run-1',location:'file.ts:42',message:'desc',data:{},timestamp:Date.now()})+'\n');
// #endregion debug-mode-log
```

### 异步日志（避免阻塞）

```typescript
// #region debug-mode-log
(async()=>{try{await fetch('http://127.0.0.1:7491',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({hypothesisId:'H1',runId:'run-1',location:'file.ts:42',message:'desc',data:{key:value},timestamp:Date.now()})})}catch{}})();
// #endregion debug-mode-log
```

## Python

### 直接写文件（推荐）

```python
# region debug-mode-log
import json,time,os;open(os.path.expanduser('~/.codeflicker/debug.log'),'a').write(json.dumps({"hypothesisId":"H1","runId":"run-1","location":"file.py:42","message":"desc","data":{},"timestamp":int(time.time()*1000)})+'\n')
# endregion debug-mode-log
```

### 多行格式

```python
# region debug-mode-log
import json
import time
import os
with open(os.path.expanduser('~/.codeflicker/debug.log'), 'a') as f:
    f.write(json.dumps({
        "hypothesisId": "H1",
        "runId": "run-1",
        "location": "file.py:42",
        "message": "process_data START",
        "data": {"input_len": len(data)},
        "timestamp": int(time.time() * 1000)
    }) + '\n')
# endregion debug-mode-log
```

### HTTP POST 方式

```python
# region debug-mode-log
import json,time,urllib.request;urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:7491',json.dumps({"hypothesisId":"H1","runId":"run-1","location":"file.py:42","message":"desc","data":{},"timestamp":int(time.time()*1000)}).encode(),{'Content-Type':'application/json'}))
# endregion debug-mode-log
```

## Go

### 直接写文件

```go
// region debug-mode-log
if f,_:=os.OpenFile(os.Getenv("HOME")+"/.codeflicker/debug.log",os.O_APPEND|os.O_CREATE|os.O_WRONLY,0644);f!=nil{json.NewEncoder(f).Encode(map[string]interface{}{"hypothesisId":"H1","runId":"run-1","location":"file.go:42","message":"desc","data":nil,"timestamp":time.Now().UnixMilli()});f.Close()}
// endregion debug-mode-log
```

### 多行格式

```go
// region debug-mode-log
func() {
    home, _ := os.UserHomeDir()
    f, err := os.OpenFile(home+"/.codeflicker/debug.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        return
    }
    defer f.Close()
    json.NewEncoder(f).Encode(map[string]interface{}{
        "hypothesisId": "H1",
        "runId":        "run-1",
        "location":     "file.go:42",
        "message":      "handleRequest START",
        "data":         map[string]interface{}{"reqId": reqId},
        "timestamp":    time.Now().UnixMilli(),
    })
}()
// endregion debug-mode-log
```

## Java

### 直接写文件

```java
// region debug-mode-log
try{java.nio.file.Files.write(java.nio.file.Paths.get(".codeflicker/debug.log"),("{\"hypothesisId\":\"H1\",\"runId\":\"run-1\",\"location\":\"File.java:42\",\"message\":\"desc\",\"data\":{},\"timestamp\":"+System.currentTimeMillis()+"}\n").getBytes(),java.nio.file.StandardOpenOption.CREATE,java.nio.file.StandardOpenOption.APPEND);}catch(Exception e){}
// endregion debug-mode-log
```

### 多行格式

```java
// region debug-mode-log
try {
    String log = String.format(
        "{\"hypothesisId\":\"H1\",\"runId\":\"run-1\",\"location\":\"File.java:42\",\"message\":\"processRequest\",\"data\":{\"id\":%d},\"timestamp\":%d}\n",
        id, System.currentTimeMillis()
    );
    java.nio.file.Files.write(
        java.nio.file.Paths.get(".codeflicker/debug.log"),
        log.getBytes(),
        java.nio.file.StandardOpenOption.CREATE,
        java.nio.file.StandardOpenOption.APPEND
    );
} catch (Exception e) {}
// endregion debug-mode-log
```

## Rust

### 直接写文件

```rust
// region debug-mode-log
if let Ok(mut f) = std::fs::OpenOptions::new().create(true).append(true).open(".codeflicker/debug.log") {
    use std::io::Write;
    let _ = writeln!(f, r#"{{"hypothesisId":"H1","runId":"run-1","location":"file.rs:42","message":"desc","data":{{}},"timestamp":{}}}"#, std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_millis());
}
// endregion debug-mode-log
```

## C/C++

### C（直接写文件）

```c
// region debug-mode-log
{FILE*f=fopen(".codeflicker/debug.log","a");if(f){fprintf(f,"{\"hypothesisId\":\"H1\",\"runId\":\"run-1\",\"location\":\"file.c:42\",\"message\":\"desc\",\"data\":{},\"timestamp\":%ld}\n",(long)time(NULL)*1000);fclose(f);}}
// endregion debug-mode-log
```

### C++

```cpp
// region debug-mode-log
{std::ofstream f(".codeflicker/debug.log",std::ios::app);if(f)f<<"{\"hypothesisId\":\"H1\",\"runId\":\"run-1\",\"location\":\"file.cpp:42\",\"message\":\"desc\",\"data\":{},\"timestamp\":"<<std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count()<<"}\n";}
// endregion debug-mode-log
```

## Ruby

```ruby
# region debug-mode-log
File.open('.codeflicker/debug.log','a'){|f|f.puts({hypothesisId:'H1',runId:'run-1',location:'file.rb:42',message:'desc',data:{},timestamp:(Time.now.to_f*1000).to_i}.to_json)}
# endregion debug-mode-log
```

## PHP

```php
// region debug-mode-log
file_put_contents('.codeflicker/debug.log',json_encode(['hypothesisId'=>'H1','runId'=>'run-1','location'=>'file.php:42','message'=>'desc','data'=>[],'timestamp'=>round(microtime(true)*1000)])."\n",FILE_APPEND);
// endregion debug-mode-log
```

## Shell/Bash

```bash
# region debug-mode-log
echo '{"hypothesisId":"H1","runId":"run-1","location":"script.sh:42","message":"desc","data":{},"timestamp":'$(date +%s%3N)'}' >> .codeflicker/debug.log
# endregion debug-mode-log
```

## 常见场景模板

### 函数入口

```typescript
// #region debug-mode-log
fetch('http://127.0.0.1:7491',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({hypothesisId:'H1',runId:'run-1',location:'file.ts:42',message:'FUNCTION_NAME ENTRY',data:{arg1,arg2},timestamp:Date.now()})}).catch(()=>{});
// #endregion debug-mode-log
```

### 函数出口

```typescript
// #region debug-mode-log
fetch('http://127.0.0.1:7491',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({hypothesisId:'H1',runId:'run-1',location:'file.ts:99',message:'FUNCTION_NAME EXIT',data:{returnValue:result},timestamp:Date.now()})}).catch(()=>{});
// #endregion debug-mode-log
```

### 条件分支

```typescript
// #region debug-mode-log
fetch('http://127.0.0.1:7491',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({hypothesisId:'H2',runId:'run-1',location:'file.ts:55',message:'BRANCH: condition===true',data:{condition:someValue},timestamp:Date.now()})}).catch(()=>{});
// #endregion debug-mode-log
```

### 状态变化

```typescript
// #region debug-mode-log
fetch('http://127.0.0.1:7491',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({hypothesisId:'H3',runId:'run-1',location:'file.ts:70',message:'STATE CHANGE',data:{before:oldState,after:newState},timestamp:Date.now()})}).catch(()=>{});
// #endregion debug-mode-log
```

### 异常捕获

```typescript
// #region debug-mode-log
fetch('http://127.0.0.1:7491',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({hypothesisId:'H4',runId:'run-1',location:'file.ts:80',message:'ERROR CAUGHT',data:{error:err.message,stack:err.stack},timestamp:Date.now()})}).catch(()=>{});
// #endregion debug-mode-log
```
