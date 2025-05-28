/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'client/templates/client/*.html',
    'core/templates/core/*.html',
    'dashboard/templates/dashboard/*.html',
    'lead/templates/lead/*.html',
    'team/templates/team/*.html',
    'user_profile/templates/user_profile/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

