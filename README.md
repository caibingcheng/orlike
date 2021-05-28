# OrLike

![GitHub](https://img.shields.io/github/license/caibingcheng/orlike)
![GitHub release (latest by date)](https://img.shields.io/github/release/caibingcheng/orlike)

使用LeanCloud, 部署在vercel的博客点赞插件.

# Deployment

在这里可以将OrLike部署到你的Vercel账户上.

[![Deploy to Vercel](https://camo.githubusercontent.com/f209ca5cc3af7dd930b6bfc55b3d7b6a5fde1aff/68747470733a2f2f76657263656c2e636f6d2f627574746f6e)](https://vercel.com/import/project?template=https://github.com/caibingcheng/orlike)


# Usage

在你期望嵌入```OrLike```的页面加入以下链接:
```JavaScript
<script src="https://cdn.jsdelivr.net/gh/caibingcheng/orlike@master/orlike.js"></script>
```
当然, 也可以使用自己的CDN. 本项目也依赖JQuery, 所以别忘记引用JQuery:
```JavaScript
<script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
```

接下来, 在你期望嵌入```OrLike```的位置加上一个```div```标签, 并且加上```class```或者```id```:
```HTML
<div class="orlike-box"></div>
```

然后在合适的地方初始化```OrLike```:
```HTML
<script>
    new OrLike({ serverUrl: "http://orlike-caibingcheng.vercel.app/", el: ".orlike-box" });
</script>
```

目前初始化需要的参数:
- ```serverUrl```: Vercel服务地址
- ```el```: 放```orlike```的```div```名字(```class```或```id```)
- ```days```: 用户id保存的时间, 默认是30天

到此为止, 本地工作已经做完了, 现在需要创建LeanCloud账户, 可以参考[Valine](https://valine.js.org/quickstart.html)的配置方法.

创建账户并且新建应用之后， 需要**给应用添加一个名为```OrLike```的class**, 然后再拿到LeanCloud的```APP ID``` 和 ```APP Key```填入到Vercel的环境变量.

- ```APPID``` 对应 ```APP ID```
- ```APPKEY``` 对应 ```APP Key```

然后部署OrLike就可以正常工作了.

# Todo & Contributes
项目初期, 还有很多想象空间, 加油↖(^ω^)↗
