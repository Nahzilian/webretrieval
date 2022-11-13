import { useState, useEffect } from 'react'
import SearchBar from '../components/SearchBar'
import useInterval from '../hooks/useInterval'
import useQuery from '../hooks/useQuery'
import { queryData } from '../api/search'
import { useNavigate, useLocation } from 'react-router-dom'
import Card from '../components/Card'
import Pagination from '../components/Pagination'
import './stylesheets/homepage.css'

const defaultPlaceholder = [
    "How to be top G?",
    "How to make tikka masala?",
    "Software development",
    "How to get good at games?",
]

const pagination = {
    currentPage: 0,
    totalPages: 20,
}

const Homepage = () => {
    const query = useQuery()
    const navigate = useNavigate()
    const { state } = useLocation()
    const [displayResult, setDisplayResult] = useState(false)
    const [searchResult, setSearchResult] = useState([])
    const [searchBar, setSearchBar] = useState({
        placeholder: defaultPlaceholder[0],
        value: ""
    })

    useInterval(() => {
        let randomIndex = Math.floor(Math.random() * defaultPlaceholder.length)
        setSearchBar(prev => ({ ...prev, placeholder: defaultPlaceholder[randomIndex] }))
    }, 2500)

    useEffect(() => {
        let pageQuery = query.get('q')

        if (state) {
            let { data } = state
            if (data && data.length && data.length > 0)
                setSearchResult(data)
            else
                if (pageQuery)
                    queryData(pageQuery).then((res) => setSearchResult(res.data))

        }
        if (pageQuery) {
            setDisplayResult(true)
            setSearchBar(prev => ({ ...prev, value: pageQuery }))
        }
    }, [query, state])

    // Form actions

    const onSubmit = () => {
        const pageQuery = {
            query: searchBar.value
        }
        queryData(pageQuery).then((res) => navigate(`/?q=${searchBar.value}`, { state: { data: res.data } }))
    }

    const onPageChange = (pageSetting) => {
        const { currentPage } = pageSetting
        const pageQuery = {
            query: searchBar.value,
            page: currentPage
        }
        queryData(pageQuery).then((res) => {
            setSearchResult(res.data)
        })
        // setPagination(page)
    }

    const onChange = (e) => setSearchBar(prev => ({ ...prev, value: e.target.value }))

    // If the query has been hit, change the page format
    if (displayResult)
        return (
            <section className='homepage result'>
                <div className='search-box-wrapper result'>
                    <SearchBar
                        minimize
                        {...searchBar}
                        onChange={onChange}
                        onSubmit={onSubmit}
                    />
                </div>
                {searchResult.length > 0 &&
                    searchResult.map((item, key) =>
                        <Card key={key} {...item} />)}
                <Pagination pageSetting={pagination} callback={onPageChange} />
            </section>
        )

    return (
        <section className="homepage">
            <div className='search-box-wrapper'>
                <h1>Queria</h1>
                <SearchBar
                    {...searchBar}
                    onChange={onChange}
                    onSubmit={onSubmit}
                />
            </div>
        </section>
    )
}

export default Homepage;