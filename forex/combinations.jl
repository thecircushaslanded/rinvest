using DataFrames

df = readtable("/Users/Robert/Code/forex/test.csv")

function returnpercent(comb::Array, row::Int)
    return reduce(*, [1+df[row, c] for c in comb])
end

hedges = DataFrame( broker=String[], c1=String[], c2=String[], c3=String[], c4=String[], r=Float32[] )
for k in 1:size(df)[1]
    # Find best combination in this row
    broker = df[k,:broker]
    choices = names(df)[2:end]
    # All combinations
    combs = combinations(choices,4)
    for comb in combs 
        ca = split(string(comb), r"\[|\:|\_|\,|\]", false)
        if (ca[2]==ca[3]) & (ca[4]==ca[5]) & (ca[6]==ca[7]) & (ca[8]==ca[1]) &
           (ca[1]!=ca[4]) & (ca[3]!=ca[6]) & (ca[5]!=ca[8]) & (ca[7]!=ca[2])
                c1, c2, c3, c4 = [string(c) for c in comb]
                r = returnpercent(comb, k)
                push!(hedges, [broker c1 c2 c3 c4 r])
        end
    end
end


sort!(hedges, cols=[:r], rev=true)
print(hedges)
