# Frontend
A browser application that provides a dashboard and a graph for visualizing the data provided by the backend.

## Main tools
- Application is created with [Vue 3](https://vuejs.org/)
- [VueX](https://vuex.vuejs.org/) is used for state management
- The graph is created with [v-network-graph](https://github.com/dash14/v-network-graph)
- Directed acyclic graph layout is generated with [Dagre](https://github.com/dagrejs/dagre)
- [Bootsrap 5](https://getbootstrap.com/) and [Bootsrap icons](https://icons.getbootstrap.com/)  are used for styling
- [Axios](https://axios-http.com/) is used for HTTP requests and request handling
- [Pretty-bytes](https://github.com/sindresorhus/pretty-bytes) makes bytes look pretty


## How to run

Recommended to be run with the docker-compose files in the repository root directory.

In order to work properly:
- VUE_APP_BACKEND_URL ENV variable must be defined and refer to the backend api root URL.

All requirements are configured in the docker-compose files. docker-compose.dev.yml is intended for development and it supports debugging. docker-compose.yml is intended for all other uses.

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```
