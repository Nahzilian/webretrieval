import usePagination from '../hooks/usePagination'
import './stylesheets/pagination.css'

const Pagination = (props) => {
    const {
        pageSetting = {},
        callback = () => { }
    } = props

    const {
        pageObject,
        pageDistribution,
        onPageChange,
        nextPage,
        prevPage
    } = usePagination(pageSetting, callback)

    const { currentPage } = pageObject

    return (<div className='pagination-wrapper'>
        <div className='pagination'>
            <div className="" onClick={prevPage}>
                <i className="fa-solid fa-arrow-left"></i>
            </div>
            {pageDistribution.map((value, key) =>
                <div
                    key={key}
                    className={`pagination-item ${currentPage === value ? 'active' : ''}`}
                    onClick={() => onPageChange(value)}>
                    <span>{value + 1}</span>
                </div>)}
            <div className="" onClick={nextPage}>
                <i className="fa-solid fa-arrow-right"></i>
            </div>
        </div>
    </div>)
}

export default Pagination;