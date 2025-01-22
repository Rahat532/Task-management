/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //Templates At the project level
    "./**/templates/**/*.html", //Templates Inside apps
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

