import { useState, useEffect } from 'react'
import SearchBar from '../components/SearchBar'
import useInterval from '../hooks/useInterval'
import useQuery from '../hooks/useQuery'
import { queryData } from '../api/search'
import { useNavigate, useLocation } from 'react-router-dom'
import Card from '../components/Card'
import './stylesheets/homepage.css'

const defaultPlaceholder = [
    "Some input 1",
    "Some input 2",
    "Some input 3",
    "Some input 4",
]

const Homepage = () => {
    const query = useQuery()
    const navigate = useNavigate()
    const { state } = useLocation()
    const [displayResult, setDisplayResult] = useState(false)
    const [searchBar, setSearchBar] = useState({
        placeholder: defaultPlaceholder[0],
        value: ""
    })
    const [searchResult, setSearchResult] = useState([])

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
                if (query)
                    queryData(query).then((res) => setSearchResult(res.data))

        }
        if (pageQuery) {
            setDisplayResult(true)
            setSearchBar(prev => ({ ...prev, value: pageQuery }))
        }
    }, [query, state])

    // Form actions

    const onSubmit = () => {
        const query = {
            query: searchBar.value
        }
        queryData(query).then((res) => navigate(`/?q=${searchBar.value}`, { state: { data: res.data } }))
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
                <div>
                    {searchResult.length > 0 && searchResult.map((item, key) => <Card key={key} {...item}/>)}
                </div>
            </section>
        )

    return (
        <section className="homepage">
            <div className='search-box-wrapper'>
                <h1>Some text</h1>
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