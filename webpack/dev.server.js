process.traceDeprecation = true;
const path = require('path');
const WebpackCommon = require('./webpack.common');
const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-webpack-plugin');
const CircularDependencyPlugin = require('circular-dependency-plugin');
var isPublicDomainDefined = process.env.KOBOFORM_PUBLIC_SUBDOMAIN &&
  process.env.PUBLIC_DOMAIN_NAME;
var publicDomain = isPublicDomainDefined ? process.env.KOBOFORM_PUBLIC_SUBDOMAIN
  + '.' + process.env.PUBLIC_DOMAIN_NAME : 'localhost';
var publicPath = 'http://' + publicDomain + ':3000/static/compiled/';

module.exports = WebpackCommon({
  mode: 'development',
  optimization: {
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },
  entry: {
    app: ['./jsapp/js/main.es6'],
    browsertests: path.resolve(__dirname, '../test/index.js'),
  },
  output: {
    library: 'KPI',
    path: path.resolve(__dirname, '../jsapp/compiled/'),
    publicPath: publicPath,
    filename: '[name]-[contenthash].js',
  },
  devServer: {
    devMiddleware: {
      publicPath: publicPath,
    },
    allowedHosts: 'all',
    hot: true,
    headers: {'Access-Control-Allow-Origin': '*'},
    port: 3000,
    host: '0.0.0.0',
  },
  devtool: 'eval-source-map',
  plugins: [
    new CircularDependencyPlugin({
      exclude: /a\.js|node_modules/,
      include: /jsapp/,
      failOnError: false,
      allowAsyncCycles: false,
      cwd: process.cwd(),
    }),
    new ReactRefreshWebpackPlugin(),
  ],
});
