#!/usr/bin/python

import psycopg2


def create_database():
    commands = (
        """
    CREATE TABLE IF NOT EXISTS public.customer_account
    (
        customer_id integer NOT NULL DEFAULT nextval('customer_account_customer_id_seq'::regclass),
        citizen_id character varying(11) COLLATE pg_catalog."default" NOT NULL,
        customer_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
        customer_surname character varying(50) COLLATE pg_catalog."default" NOT NULL,
        customer_mail character varying(50) COLLATE pg_catalog."default" NOT NULL,
        customer_password character varying(250) COLLATE pg_catalog."default" NOT NULL,
        customer_age integer NOT NULL,
        customer_province character varying(20) COLLATE pg_catalog."default" NOT NULL,
        customer_telephone character varying(15) COLLATE pg_catalog."default" NOT NULL,
        register_date timestamp without time zone NOT NULL,
        reliability_count integer,
        CONSTRAINT customer_account_pkey PRIMARY KEY (customer_id),
        CONSTRAINT customer_account_citizen_id_key UNIQUE (citizen_id),
        CONSTRAINT customer_account_citizen_id_fkey FOREIGN KEY (citizen_id)
            REFERENCES public.customer (customer_citizen_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
        """
        ,
        """
    CREATE TABLE IF NOT EXISTS public.seller_account
    (
        seller_id integer NOT NULL DEFAULT nextval('seller_account_seller_id_seq'::regclass),
        person_id character varying(11) COLLATE pg_catalog."default" NOT NULL,
        seller_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
        seller_surname character varying(50) COLLATE pg_catalog."default" NOT NULL,
        seller_mail character varying(50) COLLATE pg_catalog."default" NOT NULL,
        seller_password character varying(250) COLLATE pg_catalog."default" NOT NULL,
        seller_age integer NOT NULL,
        seller_province character varying(15) COLLATE pg_catalog."default" NOT NULL,
        seller_telephone character varying(15) COLLATE pg_catalog."default" NOT NULL,
        account_type boolean NOT NULL,
        register_time timestamp without time zone NOT NULL,
        CONSTRAINT seller_account_pkey PRIMARY KEY (seller_id),
        CONSTRAINT seller_account_person_id_key UNIQUE (person_id),
        CONSTRAINT seller_account_person_id_fkey FOREIGN KEY (person_id)
            REFERENCES public.seller (seller_citizen_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
        """
        ,

        """
    CREATE TABLE IF NOT EXISTS public.customer
    (
        customer_citizen_id character varying(11) COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT customer_pkey PRIMARY KEY (customer_citizen_id)
    )
        """
        ,
        """
    CREATE TABLE IF NOT EXISTS public.seller
    (
        seller_citizen_id character varying(11) COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT seller_pkey PRIMARY KEY (seller_citizen_id)
    )
        """
        ,
        """
        
    CREATE TABLE IF NOT EXISTS public.premium_seller
    (
        premium_id integer NOT NULL DEFAULT nextval('premium_seller_premium_id_seq'::regclass),
        supplier_no integer NOT NULL,
        cars_number integer NOT NULL,
        CONSTRAINT premium_seller_pkey PRIMARY KEY (premium_id),
        CONSTRAINT premium_seller_supplier_no_key UNIQUE (supplier_no),
        CONSTRAINT premium_seller_supplier_no_fkey FOREIGN KEY (supplier_no)
            REFERENCES public.seller_account (seller_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
        """
        ,
        """
        CREATE TABLE IF NOT EXISTS public.standard_seller
    (
        standard_id integer NOT NULL DEFAULT nextval('standard_seller_standard_id_seq'::regclass),
        vendor_no integer NOT NULL,
        car_number boolean NOT NULL,
        CONSTRAINT standard_seller_pkey PRIMARY KEY (standard_id),
        CONSTRAINT standard_seller_vendor_no_key UNIQUE (vendor_no),
        CONSTRAINT standard_seller_vendor_no_fkey FOREIGN KEY (vendor_no)
            REFERENCES public.seller_account (seller_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
        """
        ,
        """
    CREATE TABLE IF NOT EXISTS public.reliability_ratio
    (
        ratio_id integer NOT NULL DEFAULT nextval('reliability_ratio_ratio_id_seq'::regclass),
        account_no integer NOT NULL,
        number_of_votes integer NOT NULL,
        ratio double precision NOT NULL,
        CONSTRAINT reliability_ratio_pkey PRIMARY KEY (ratio_id),
        CONSTRAINT reliability_ratio_account_no_fkey FOREIGN KEY (account_no)
            REFERENCES public.seller_account (seller_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
        """
        ,
        """
        CREATE TABLE IF NOT EXISTS public.cars
    (
        product_no integer NOT NULL DEFAULT nextval('cars_product_no_seq'::regclass),
        owner_id integer NOT NULL,
        car_brand character varying(30) COLLATE pg_catalog."default" NOT NULL,
        car_model character varying(40) COLLATE pg_catalog."default" NOT NULL,
        fuel_type character varying(15) COLLATE pg_catalog."default" NOT NULL,
        km integer NOT NULL,
        car_year integer NOT NULL,
        photo bytea NOT NULL,
        CONSTRAINT cars_pkey PRIMARY KEY (product_no),
        CONSTRAINT cars_owner_id_fkey FOREIGN KEY (owner_id)
            REFERENCES public.seller_account (seller_id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
        """
        ,
        """
    CREATE TABLE IF NOT EXISTS public.online_market
    (
        publish_id integer NOT NULL DEFAULT nextval('online_market_publish_id_seq'::regclass),
        product_id integer NOT NULL,
        price integer NOT NULL,
        sell_rent boolean NOT NULL,
        title text COLLATE pg_catalog."default" NOT NULL,
        description text COLLATE pg_catalog."default",
        CONSTRAINT online_market_pkey PRIMARY KEY (publish_id),
        CONSTRAINT online_market_product_id_key UNIQUE (product_id),
        CONSTRAINT online_market_product_id_fkey FOREIGN KEY (product_id)
            REFERENCES public.cars (product_no) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )
        """   
        )
    conn = None
    try:
        conn = psycopg2.connect(host = "localhost", database="gallery_system", user = "postgres", password = "12bizimkiler34")
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_database()