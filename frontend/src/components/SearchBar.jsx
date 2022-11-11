import './stylesheets/searchbar.css'

const SearchBar = (props) => {
    const {
        onChange = () => { },
        value = '',
        placeholder = '',
        minimize = false,
        onSubmit = () => { }
    } = props

    const onSearch = (e) => {
        e.preventDefault()
        onSubmit()
    }

    return (
        <form className='search-bar-wrapper' onSubmit={onSearch}>
            <input className={`search-bar ${minimize ? 'minimize' : ''}`}
                value={value}
                onChange={onChange}
                placeholder={placeholder} />

            <i className={`fa-regular fa-magnifying-glass-arrow-right search-icon ${minimize ? 'minimize' : ''}`}
                style={{ fontSize: 40 }} />
        </form>);
}

export default SearchBar;