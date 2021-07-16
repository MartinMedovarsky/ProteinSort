import { useEffect, useState } from 'react'
import axios from 'axios'

export function useProdSingle(query) {

    console.log("Query: " + query)

    useEffect(() => {
        let cancel
        axios({
            method: 'GET',
            url: 'http://localhost:5000/products/single',
            params: { id: query },
            cancelToken: new axios.CancelToken(c => cancel = c)    
        }).then(res => {
            console.log(res.data)
        }).catch(e => {
            if (axios.isCancel(e)) return
        })
        return () => cancel()
    }, [query])

    return null
}

export function useProdComplex() {

    return null
}

