/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {
      colors: {
        customBlue: '#007BFF',
        customGreen: '#28A745',
        customRed: '#DC3545',
      },
      backgroundColor: {
        'bg-customBlue': '#007BFF',
        primary: {"50":"#eff6ff","100":"#dbeafe","200":"#bfdbfe","300":"#93c5fd","400":"#60a5fa","500":"#3b82f6","600":"#2563eb","700":"#1d4ed8","800":"#1e40af","900":"#1e3a8a","950":"#172554"}
      },
    },
  },
  plugins: [
    require('flowbite/plugin'),
    require('flowbite/plugin')({
      charts: true,
  }),
  ],
}

