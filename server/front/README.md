# vue-abchat

[![npm version](https://img.shields.io/npm/v/vue-abchat.svg?style=flat-square)](https://www.npmjs.org/package/vue-abchat)
[![install size](https://packagephobia.now.sh/badge?p=vue-abchat)](https://packagephobia.now.sh/result?p=vue-abchat)
[![npm downloads](https://img.shields.io/npm/dm/vue-abchat.svg?style=flat-square)](http://npm-stat.com/charts.html?package=vue-abchat)



## Intro

**`vue-abchat`**은

인공지능 챗봇 서비스를 편하게 구현하기 위한 vue.js component 입니다.

**`vue-abchat`**을 활용하면 ABC 보다 더 쉽게 챗봇을 서비스할 수 있습니다.

챗봇 서버에 Rest-api 요청으로 메세지를 보내면 응답 결과를 받아 chat 화면에 띄워줍니다.



현재 베타버전입니다.



데모 페이지: `예정`



## Installation

##### npm / node.js

- Install

```
npm install vue-abchat
```

- Usage

##### *.vue

```vue
<template>
    <abchat :BASE_URL="'http://localhost:8000/'"></abchat>
</template>
<script>
// get component from node_modules
import abchat from '@/components/vue-abchat.vue'
export default {
  name: 'app',
  // add component
  components: {
    abchat
  }
}
</script>
```



##### CDN

- Install

*We use axios library*

```html
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<script src="https://unpkg.com/vue-abchat/dist/abchat.min.js"></script>
```

- Usage

```html
<body>
    <div id="app">
        <abchat :base_url="'http://localhost:8000/'"></abchat>
    </div>
</body>
<script type="text/javascript">
    var app = new Vue({
        el: '#app'
    })
</script>
```



## Usage

컴포넌트 형태로 배포하였기 때문에 사용을 원하는 vue 파일에서 직접 import 한 후 사용하시면 됩니다.



##### props로 customizing 가능

```vue
<template>
    <abchat :base_url="'http://localhost:8000/'" :title="'sjchat'" button_title="'hello'"></abchat>
</template>
```



##### 현재 지원하는 props 목록

| props                  | 역할                                    | 입력타입 |
| ---------------------- | --------------------------------------- | -------- |
| :base_url `(required)` | 챗봇을 위한 api 서버 url                | String   |
| :width                 | 채팅창의 가로 길이를 지정 (px)          | Number   |
| :height                | 채팅창의 세로 길이를 지정(px)           | Number   |
| :title                 | 채팅창 상단의 제목                      | String   |
| :button_title          | 채팅창 최소화 시 버튼에 나타나는 텍스트 | String   |



##### attribute로 customizing 가능

```vue
<template>
    <abchat :base_url="'http://localhost:8000/'" top left></abchat>
</template>
```



##### 지원하는 attribute 목록

| attribute          | 역할                                 |
| ------------------ | ------------------------------------ |
| top                | css {position: fixed; top: 30px;}    |
| bottom `(Default)` | css {position: fixed; bottom: 30px;} |
| left               | css {position: fixed; left: 30px;}   |
| right`(Default)`   | css {position: fixed; right: 30px;}  |



---

#### 데이터 요청 및 응답 방식

##### `Rest-api`

method : `GET`

요청방식 : `BASE_URL/{{message}}`

요청결과 예시:

```json
{
  "result": "POS"
}
```



## 예시화면



##### 버튼을 클릭하면 채팅창이 열립니다.

![ex4](https://user-images.githubusercontent.com/45934052/65669904-500cdf00-e07f-11e9-895e-d55bd923d66c.png)

##### 채팅창 기본 화면

![ex1](https://user-images.githubusercontent.com/45934052/65669833-34093d80-e07f-11e9-9a08-06b2e132e27e.png)

##### 채팅을 입력하면 Rest-api 형식으로 서버에 요청한 뒤 응답된 결과를 출력합니다.

![ex2](https://user-images.githubusercontent.com/45934052/65669864-3ff4ff80-e07f-11e9-9b00-dc54240c5760.png)

##### C버튼을 누르면 채팅을 지울 수 있습니다.

![ex1](https://user-images.githubusercontent.com/45934052/65669833-34093d80-e07f-11e9-9a08-06b2e132e27e.png)





# License

[MIT](LICENSE)


