# wifi monitor
```
wifi_monitor/  
├── wifi_data/utils  
    ├── __init__.py  
    ├── database.py  
    ├── monitor.py  
    ├── parser.py  
    └── wifi.py 
```
主要有一下几个功能：
*解析文件， 获取文件数据
*数据格式处理
*数据库插入数据
*检测文件变化

# parser.py
解析传入的zip包，通过WiFiMeta类， 解析zip包中的xml文件， 获取相应的数据， 然后通过CSVParser类，对zip包中的数据文件进行解析，
获取到想要的数据格式

#wifi.py
在WiFiData类下， 对数据进行验证，验证数据的type, max_length, 是否必填等条件，还可以通过wifi类下的方法，处理数据插入数据库是的格式

#database.py
拿到处理的数据，发送到kafka中

#monitor.py
开启检测目标文件夹中是否有所变化，如果有变化，会按照调用顺序执行以上功能