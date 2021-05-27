# OrLike

使用LeanCloud, 部署在vercel的博客点赞插件.

# Usage

在你期望嵌入```OrLike```的页面加入以下链接:
```JavaScript
<script src="https://cdn.jsdelivr.net/gh/caibingcheng/orlike@master/orlike.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/caibingcheng/orlike@master/orlike.css">
```

在你期望嵌入```OrLike```的位置加上一个```div```标签, 并且加上```class```或者```id```
```
<div class="orlike-box"></div>
```

然后在合适的地方初始化```OrLike```
```
<script>
    new OrLike({ serverUrl: "http://orlike-caibingcheng.vercel.app/", el: ".orlike-box" });
</script>
```

目前初始化需要两个参数
- ```serverUrl```: 服务地址
- ```el```放```orlike```的```div```名字(```class```或```id```)

# Deployment

在你自己的Vercel账户上部署OrLike吧~

[![Deploy to Vercel](https://camo.githubusercontent.com/f209ca5cc3af7dd930b6bfc55b3d7b6a5fde1aff/68747470733a2f2f76657263656c2e636f6d2f627574746f6e)](https://vercel.com/import/project?template=https://github.com/caibingcheng/orlike)
