
module.exports = {
  content: [
    "./src/web/templates/**/*.html",
    "./src/web/static/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

