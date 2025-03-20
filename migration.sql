--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 17.4 (Ubuntu 17.4-1.pgdg24.04+2)

CREATE DATABASE ETL;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: mongo_data; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA mongo_data;


ALTER SCHEMA mongo_data OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: eventlogs; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.eventlogs (
    event_id character varying NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    event_type character varying(50) NOT NULL,
    details text
);


ALTER TABLE mongo_data.eventlogs OWNER TO postgres;

--
-- Name: moderationqueue; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.moderationqueue (
    review_id character varying NOT NULL,
    user_id character varying NOT NULL,
    product_id character varying NOT NULL,
    review_text text NOT NULL,
    rating integer,
    moderation_status character varying(20) NOT NULL,
    submitted_at timestamp without time zone NOT NULL,
    CONSTRAINT moderationqueue_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE mongo_data.moderationqueue OWNER TO postgres;

--
-- Name: moderationqueue_flags; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.moderationqueue_flags (
    review_id character varying NOT NULL,
    flag text NOT NULL
);


ALTER TABLE mongo_data.moderationqueue_flags OWNER TO postgres;

--
-- Name: productpricehistory; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.productpricehistory (
    product_id character varying NOT NULL,
    current_price numeric(10,2) NOT NULL,
    currency character varying(3) NOT NULL
);


ALTER TABLE mongo_data.productpricehistory OWNER TO postgres;

--
-- Name: productpricehistory_price_changes; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.productpricehistory_price_changes (
    product_id character varying NOT NULL,
    change_date timestamp without time zone NOT NULL,
    change_price numeric(10,2) NOT NULL
);


ALTER TABLE mongo_data.productpricehistory_price_changes OWNER TO postgres;

--
-- Name: searchqueries; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.searchqueries (
    query_id character varying NOT NULL,
    user_id character varying NOT NULL,
    query_text text NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    results_count integer NOT NULL
);


ALTER TABLE mongo_data.searchqueries OWNER TO postgres;

--
-- Name: searchqueries_filters; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.searchqueries_filters (
    query_id character varying NOT NULL,
    filter text NOT NULL
);


ALTER TABLE mongo_data.searchqueries_filters OWNER TO postgres;

--
-- Name: supporttickets; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.supporttickets (
    ticket_id character varying NOT NULL,
    user_id character varying NOT NULL,
    status character varying(20) NOT NULL,
    issue_type character varying(50) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE mongo_data.supporttickets OWNER TO postgres;

--
-- Name: supporttickets_messages; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.supporttickets_messages (
    ticket_id character varying NOT NULL,
    message text NOT NULL
);


ALTER TABLE mongo_data.supporttickets_messages OWNER TO postgres;

--
-- Name: userrecommendations; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.userrecommendations (
    user_id character varying NOT NULL,
    last_updated timestamp without time zone NOT NULL
);


ALTER TABLE mongo_data.userrecommendations OWNER TO postgres;

--
-- Name: userrecommendations_products; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.userrecommendations_products (
    user_id character varying NOT NULL,
    recommended_product text NOT NULL
);


ALTER TABLE mongo_data.userrecommendations_products OWNER TO postgres;

--
-- Name: usersessions; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.usersessions (
    session_id character varying NOT NULL,
    user_id character varying NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    device text
);


ALTER TABLE mongo_data.usersessions OWNER TO postgres;

--
-- Name: usersessions_actions; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.usersessions_actions (
    session_id character varying NOT NULL,
    actions character varying NOT NULL
);


ALTER TABLE mongo_data.usersessions_actions OWNER TO postgres;

--
-- Name: usersessions_pages; Type: TABLE; Schema: mongo_data; Owner: postgres
--

CREATE TABLE mongo_data.usersessions_pages (
    session_id character varying NOT NULL,
    pages_visited character varying NOT NULL
);


ALTER TABLE mongo_data.usersessions_pages OWNER TO postgres;

--
-- Name: eventlogs eventlogs_pkey; Type: CONSTRAINT; Schema: mongo_data; Owner: postgres
--

ALTER TABLE ONLY mongo_data.eventlogs
    ADD CONSTRAINT eventlogs_pkey PRIMARY KEY (event_id);


--
-- Name: moderationqueue moderationqueue_pkey; Type: CONSTRAINT; Schema: mongo_data; Owner: postgres
--

ALTER TABLE ONLY mongo_data.moderationqueue
    ADD CONSTRAINT moderationqueue_pkey PRIMARY KEY (review_id);


--
-- Name: productpricehistory productpricehistory_pkey; Type: CONSTRAINT; Schema: mongo_data; Owner: postgres
--

ALTER TABLE ONLY mongo_data.productpricehistory
    ADD CONSTRAINT productpricehistory_pkey PRIMARY KEY (product_id);


--
-- Name: searchqueries searchqueries_pkey; Type: CONSTRAINT; Schema: mongo_data; Owner: postgres
--

ALTER TABLE ONLY mongo_data.searchqueries
    ADD CONSTRAINT searchqueries_pkey PRIMARY KEY (query_id);


--
-- Name: supporttickets supporttickets_pkey; Type: CONSTRAINT; Schema: mongo_data; Owner: postgres
--

ALTER TABLE ONLY mongo_data.supporttickets
    ADD CONSTRAINT supporttickets_pkey PRIMARY KEY (ticket_id);


--
-- Name: userrecommendations userrecommendations_pkey; Type: CONSTRAINT; Schema: mongo_data; Owner: postgres
--

ALTER TABLE ONLY mongo_data.userrecommendations
    ADD CONSTRAINT userrecommendations_pkey PRIMARY KEY (user_id);


--
-- Name: usersessions usersessions_pkey; Type: CONSTRAINT; Schema: mongo_data; Owner: postgres
--

ALTER TABLE ONLY mongo_data.usersessions
    ADD CONSTRAINT usersessions_pkey PRIMARY KEY (session_id);


--
-- PostgreSQL database dump complete
--

