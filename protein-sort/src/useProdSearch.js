import { useEffect, useState } from 'react'
import axios from 'axios'

export function useProdSingle(single) {
    const [singleProduct, setSingleProduct] = useState()

    useEffect(() => {
        setSingleProduct()

        console.log("USEPRODSINGLE SINGLE: " + single)
        let cancel
        axios({
            method: 'GET',
            url: 'http://localhost:5000/products/single',
            params: { id: single },
            cancelToken: new axios.CancelToken(c => cancel = c)    
        }).then(res => {
            setSingleProduct(res.data)
        }).catch(e => {
            if (axios.isCancel(e)) return
        })
        return () => cancel()
    }, [single])

    return { singleProduct }
}

export function useProdComplex(query, dropdown, pageNumber) {
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(false)
    const [products, setProducts] = useState([])
    const [hasMore, setHasMore] = useState(false)

    useEffect(() => {
        setProducts([])
    }, [query, dropdown])

    useEffect(() => {
        setLoading(true)
        setError(false)

        let cancel
        axios({
            method: 'GET',
            url: 'http://localhost:5000/products/complex',
            params: { search: query, dep: dropdown, page: pageNumber},
            cancelToken: new axios.CancelToken(c => cancel = c)    
        }).then(res => {
            setProducts(prevProducts => {
                //Combining new and old products in a set to remove duplicates, then converting back to array
                return [...new Set([...prevProducts, ...res.data.data])]
            })
            //Checks that products are being returned
            //If there are none then we have reached the last page
            setHasMore(res.data.data.length > 0)
            setLoading(false)
            console.log(res.data)
        }).catch(e => {
            if (axios.isCancel(e)) return
            setError(true)
        })
        return () => cancel()
    }, [query, dropdown, pageNumber])

    //console.log("Why am i getting printed multiple times")
    //console.log(products)
    return { loading, error, products, hasMore}

}

