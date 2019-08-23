# porn-detect


!!!哎！！识别不太准啊！！！！

Python 黄色、色情图片识别

简单有效的识别色情图片。

基于文献：《基于肤色特征的色情图像识别算法》 

知网: http://www.cnki.com.cn/Article/CJFDTotal-SXGX201401008.htm

百度文库: https://wenku.baidu.com/view/6ff00b5331126edb6e1a105c.html

参考： https://blog.csdn.net/sm9sun/article/details/53319959

## 效果

[效果图](./process.jpg)

## Usage

run:

```shell

python3 porn_detect.py  test_sets/3.jpg

```

output:

```shell

皮肤占比: 0.029348927875243666
皮肤占人体矩形比: 0.15305323723455083
是否识别为黄图: False

```

将变量`save_image`设置为 `True` 后，可以保存关键路径的图片。方便调试。

## License

MIT