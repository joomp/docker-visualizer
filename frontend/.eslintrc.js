module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
    'plugin:prettier/recommended',
    'plugin:jsdoc/recommended',
  ],
  parserOptions: {
    parser: '@babel/eslint-parser',
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-unused-vars': 'warn',
    'jsdoc/require-jsdoc': [
      'warn',
      {
        publicOnly: false,
        require: {
          FunctionExpression: true,
          ArrowFunctionExpression: true,
          FunctionDeclaration: true,
          MethodDefinition: true,
        },
      },
    ],
  },
  overrides: [
    {
      files: ['*.vue'],
      rules: {
        'jsdoc/require-jsdoc': 'off',
        'jsdoc/require-returns': 'off',
      },
    },
  ],
};
