# porn-detect


Python 黄色、色情图片识别

简单有效的识别色情图片。

基于文献：《基于肤色特征的色情图像识别算法》 

知网: http://www.cnki.com.cn/Article/CJFDTotal-SXGX201401008.htm

百度文库: https://wenku.baidu.com/view/6ff00b5331126edb6e1a105c.html

参考： https://blog.csdn.net/sm9sun/article/details/53319959

## Usage

run:

```shell

python3 porn_detect.py  https://img3.doubanio.com/view/note/large/public/p10795571.jpg

```

output:

```shell


('argv: ', ['porn_detect.py', 'https://img3.doubanio.com/view/note/large/public/p10795571.jpg'])
('current path: /Users/jinya/Develop/playground/github.com/porn-detect',)
('saving to: /Users/jinya/Develop/playground/github.com/porn-detect/porn_detect_temp/p10795571.jpg',)
====================100.00%
('download file path: /Users/jinya/Develop/playground/github.com/porn-detect/porn_detect_temp/p10795571.jpg',)
porn detect: https://img3.doubanio.com/view/note/large/public/p10795571.jpg socre: 7.4573523583036065  is true

```


## License

MIT