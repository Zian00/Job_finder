<b>In package.json</b><br>
if need the original server<br>
"server": "json-server --watch src/jobs.json --port 8000"

# Job Finder
#### Video Demo:  <URL HERE>
#### Description:

<b><em>Special thanks to <a href="https://www.youtube.com/@TraversyMedia">Traversy Media</a> for the beginner tutorial of React frontend.</em></b>

Traversy Media (2024) React crash course 2024, YouTube. 
Available at: https://www.youtube.com/watch?v=LDB4uaJ87e0 (Accessed: 09 June 2024). <br>

Job Finder is a web application that allows job finder to view existing jobs available in the market and he may contact the job poster via contact phone number or contact email. Meanwhile, it also allows job poster to add new job positions to the market, edit existing jobs and delete existing unwanted jobs.

This web application utilizes the following :
- Frontend - React with Tailwind CSS Framework
- Backend - Flask
- Database - Sqlite3 


Project is running in two separate folders, where the `client` folder is where frontend files are stored and the `server` folder is where backend files are stored.

The following is the tree structure of `client` folder.
- [**client**](client)
    - [**public**](client/public)
    - [**src**](client/src) - where all frontend react files are located
        - [**assets**](client/src/assets)
            - [**images**](client/src/assets/images)
                - [find_job_logo.png](client/src/assets/images/find_job_logo.png) - logo for navbar
        - [**components**](client/src/components)
            - [Hero.jsx](client/src/components/Hero.jsx) - main title for the home page
            - [Card.jsx](client/src/components/Card.jsx) - two options provided, browse or add jobs
            - [HomeCards.jsx](client/src/components/HomeCards.jsx) - contain the two cards components
            - [Joblisting.jsx](client/src/components/Joblisting.jsx) - Display each joblisting components
            - [Joblistings.jsx](client/src/components/Joblistings.jsx) - Display all `jobslistings` components available
            - [Navbar.jsx](client/src/components/Navbar.jsx)   - Display navbar component with all links navigating among pages
            - [Spinner.jsx](client/src/components/Spinner.jsx) - Used to show a spinner when loading
            - [ViewAllJobs.jsx](client/src/components/Viewalljobs.jsx) - Link to `/jobs` page
        - [**layouts**](client/src/layouts) 
            - [MainLayout.jsx](client/src/layouts/Mainlayout.jsx) - contains `Navbar` component, so that it can be called at every page
        - [**pages**](client/src/pages)
            - [AddjobPage.jsx](client/src/pages/AddjobPage.jsx) - adds new job when submitting the form
            - [EditJobPage.jsx](client/src/pages/EditJobPage.jsx) - preload the form with existing data and update the data when updated
            - [HomePage.jsx](client/src/pages/HomePage.jsx) - Contains `Hero`, `Homecards`, `Joblistings` and `ViewAllJobs` components
            - [JobPage.jsx](client/src/pages/JobPage.jsx) - Display data according to the specific ID, allows edit and delete function of the data
            - [JobsPage.jsx](client/src/pages/JobsPage.jsx) - contains `JobListings` component
            - [NotFoundPage.jsx](client/src/pages/NotFoundPage.jsx) - triggered when the page is not found
        - [App.jsx](client/src/App.jsx) - contains all pages and API calls to interact with backend
        - [index.css](client/src/index.css) - css which imports Tailwind CSS
        - [jobs.json](client/src/jobs.json) - sample data for databse to display in frontend
        - [main.jsx](client/src/main.jsx) - Called `App` component to  render the whole application 
        - [index.html](client/index.html) - script called `main.jsx`
        <br>configuration files:
        - [.eslintrc.cjs](client/.eslintrc.cjs)
        - [package.json](client/package.json)
        - [package-lock.json](client/package-lock.json)
        - [postcss.config.js](client/postcss.config.js)
        - [tailwind.config.js](client/tailwind.config.js)
        - [vite.config.js](client/vite.config.js)


The following is the tree structure of `server` folder
- [**server**](server)
    - [jobs.db](server/jobs.db)
    - [populate_data.py](server/populate_data.py)
    - [routes.py](server/routes.py)

