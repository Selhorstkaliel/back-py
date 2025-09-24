module.exports = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,jsx}',
    './components/**/*.{js,jsx}',
    './pages/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        neon: {
          100: '#3ef3fa',
          500: '#0fffc1',
          900: '#2dff8d'
        }
      }
    }
  },
  plugins: [require('tailwindcss-animate')],
};