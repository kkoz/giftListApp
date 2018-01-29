var webpack = require('webpack');
module.exports = {
  entry: [
    "./app/static/js/edit_list.js"
  ],
  output: {
    path: __dirname + '/app/static/js',
    filename: "bundle.js"
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
  ]
};