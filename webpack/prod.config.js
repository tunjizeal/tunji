const path = require('path');
const webpack = require('webpack');
const publicPath = (process.env.KPI_PREFIX === '/' ? '' : (process.env.KPI_PREFIX || '')) + '/static/compiled/';
const WebpackCommon = require('./webpack.common');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = WebpackCommon({
  mode: 'production',
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
    // Use swc to speed up the production build, too
    minimizer: [
      new TerserPlugin({
        minify: TerserPlugin.swcMinify,
        // options passed to swc: https://swc.rs/docs/configuration/minification
        terserOptions: {},
      }),
    ],
  },
  entry: {
    app: './jsapp/js/main.es6',
    browsertests: path.resolve(__dirname, '../test/index.js'),
  },
  output: {
    path: path.resolve(__dirname, '../jsapp/compiled/'),
    publicPath: publicPath,
    filename: '[name]-[contenthash].js',
  },
  plugins: [
    new webpack.SourceMapDevToolPlugin({
      filename: '[file].map',
      exclude: /vendors.*.*/,
    }),
  ],
  // mainly for hiding stylelint output
  stats: {
    all: false,
    modulesSpace: 0,
    errors: true,
    errorDetails: true,
  },
});
