Design the interface with python. Export the data from data warehouse to Web

web页面
main程序是程序入口
SQLConnector是使用pymssql连接数据库，封装了几个查询和执行操作的函数，因为仍然使用python2.7版本，存在一些字符转换的问题，所以建立了两个连接，分别使用cp936和utf-8解码
Tbl_View_Proc存储了几个更新系统存储程序的脚本
update_db将远程的数据放到本地的一个脚本
templates下是用到的网页模板, 目前设计了employee和data两个模板，前者用于增加职员，后者显示报销单明细；

