import { useState, useEffect } from 'react'

const MAX_DISPLAY = 10

const usePagination = (pageSetting = {}, callback = () => { }) => {
    const [pageObject, setPageObject] = useState({
        currentPage: 0,
        totalPages: 1,
    })
    const [pageDistribution, setPageDistribution] = useState([])

    const onPageDistributionChange = (selectedPage, totalPages) => {
        /*
            case 1: totalPages >= MAX_DISPLAY
                - Slice of array
                case a: start of array
                case b: middle of array
                case c: end of array
            case 2: totalPages < MAX_DISPLAY
                Display full
        */
        const pageDist = []
        let start = selectedPage + MAX_DISPLAY > totalPages
            ? totalPages - MAX_DISPLAY > 0
                ? totalPages - MAX_DISPLAY
                : 0
            : selectedPage
        let itemIndex = start

        while (itemIndex < MAX_DISPLAY + start) {
            if (itemIndex === totalPages)
                break

            pageDist.push(itemIndex)
            itemIndex++
        }
        setPageDistribution(pageDist)
    }

    useEffect(() => {
        if (pageSetting.totalPages) {
            let { totalPages } = pageSetting
            onPageDistributionChange(0, totalPages)
            setPageObject(prev => ({ ...prev, ...pageSetting }))
        }
    }, [pageSetting])

    const onPageChange = (page) => {
        if (page < 0 || page >= pageObject.totalPages)
            return
        onPageDistributionChange(page, pageObject.totalPages)
        setPageObject(prev => ({ ...prev, currentPage: page }))
        callback({...pageObject, currentPage: page})
    }

    const nextPage = () => onPageChange(pageObject.currentPage + 1)

    const prevPage = () => onPageChange(pageObject.currentPage - 1)

    return { pageObject, pageDistribution, onPageChange, nextPage, prevPage }
}

export default usePagination
