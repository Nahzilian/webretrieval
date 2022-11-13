import './stylesheets/card.css'

const Card = (props) => {
    const { title, description } = props
    return (<div className='card-wrapper'>
        <div className='card'>
            <div className='card-title'>
                <div>
                    <h2>{title}</h2>
                </div>
                <div className='card-icons'>
                    <i className="fa-solid fa-star"></i>
                    <i className="fa-solid fa-heart"></i>
                    <i className="fa-solid fa-share"></i>
                </div>
            </div>
            <div className='card-body'>
                <p>{description}</p>
            </div>
        </div>
    </div>)
}

export default Card;